import os
import csv
import gzip
from datetime import datetime, timedelta

class HistoryLogger:
    def __init__(self, ups_manager, log_dir='/mnt/usb_logs/nut'):
        self.ups_manager = ups_manager
        self.log_dir = log_dir

    def read_csv_rows(self, filepath, is_gz):
        fieldnames = ["timestamp", "battery_charge_pct", "battery_voltage", "input_voltage", "ups_load_pct", "ups_status"]
        rows = []
        try:
            if is_gz:
                with gzip.open(filepath, 'rt', encoding='utf-8') as f:
                    reader = csv.DictReader(f, fieldnames=fieldnames)
                    for row in reader:
                        if row.get("timestamp") == "timestamp":
                            continue
                        rows.append(row)
            else:
                with open(filepath, 'r', encoding='utf-8') as f:
                    reader = csv.DictReader(f, fieldnames=fieldnames)
                    for row in reader:
                        if row.get("timestamp") == "timestamp":
                            continue
                        rows.append(row)
        except Exception:
            pass
        return rows

    def get_history(self, ups_name, start_str=None, end_str=None):
        if start_str:
            start_str = start_str.replace('T', ' ').split('.')[0].replace('Z', '')
        else:
            start_str = (datetime.now() - timedelta(hours=24)).strftime("%Y-%m-%d %H:%M:%S")
            
        if end_str:
            end_str = end_str.replace('T', ' ').split('.')[0].replace('Z', '')
        else:
            end_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            
        collected_rows = []
        files = [
            (f'{self.log_dir}/{ups_name}.csv', False),
            (f'{self.log_dir}/{ups_name}.csv.1', False),
        ]
        for i in range(2, 6):
            files.append((f'{self.log_dir}/{ups_name}.csv.{i}.gz', True))
            
        for filepath, is_gz in files:
            if not os.path.exists(filepath):
                continue
                
            file_rows = self.read_csv_rows(filepath, is_gz)
            file_rows.reverse()
            
            reached_start = False
            for row in file_rows:
                ts = row.get('timestamp')
                if not ts:
                    continue
                if ts > end_str:
                    continue
                if ts < start_str:
                    reached_start = True
                    break
                if (row.get('battery_charge_pct') == 'NA' or not row.get('battery_charge_pct')) and row.get('battery_voltage') != 'NA':
                    row['battery_charge_pct'] = self.ups_manager.estimate_charge(
                        row['battery_voltage'],
                        row.get('ups_status', 'OL'),
                        row.get('ups_load_pct', '0')
                    )
                collected_rows.append(row)
                
            if reached_start:
                break
                
        collected_rows.reverse()
        return collected_rows

    def analyze_outages(self, ups_name, limit=10):
        collected_rows = []
        files = [
            (f'{self.log_dir}/{ups_name}.csv', False),
            (f'{self.log_dir}/{ups_name}.csv.1', False),
        ]
        for i in range(2, 6):
            files.append((f'{self.log_dir}/{ups_name}.csv.{i}.gz', True))
            
        for filepath, is_gz in files:
            if not os.path.exists(filepath):
                continue
            file_rows = self.read_csv_rows(filepath, is_gz)
            collected_rows.extend(file_rows)
                
        parsed_rows = []
        for row in collected_rows:
            timestamp_str = row.get('timestamp')
            if not timestamp_str or timestamp_str == 'timestamp':
                continue
            try:
                volt = float(row['battery_voltage']) if row.get('battery_voltage') != 'NA' else None
                load = float(row['ups_load_pct']) if row.get('ups_load_pct') != 'NA' else 0.0
                status = row.get('ups_status', 'OL')
                parsed_rows.append({
                    'timestamp': timestamp_str,
                    'voltage': volt,
                    'load': load,
                    'status': status
                })
            except Exception:
                continue
                
        parsed_rows.sort(key=lambda x: x['timestamp'])
        
        events = []
        current_event = None
        
        for i, row in enumerate(parsed_rows):
            status = row['status']
            is_ob = 'OB' in status or 'DISCHRG' in status or 'LB' in status
            
            if is_ob:
                if current_event is None:
                    pre_volts = 27.3
                    if i > 0 and parsed_rows[i-1]['voltage'] is not None:
                        pre_volts = parsed_rows[i-1]['voltage']
                        
                    current_event = {
                        'start_time': row['timestamp'],
                        'end_time': row['timestamp'],
                        'start_voltage': row['voltage'] if row['voltage'] is not None else pre_volts,
                        'end_voltage': row['voltage'],
                        'voltages': [row['voltage']] if row['voltage'] is not None else [],
                        'loads': [row['load']],
                        'count': 1
                    }
                else:
                    current_event['end_time'] = row['timestamp']
                    if row['voltage'] is not None:
                        current_event['end_voltage'] = row['voltage']
                        current_event['voltages'].append(row['voltage'])
                    current_event['loads'].append(row['load'])
                    current_event['count'] += 1
            else:
                if current_event is not None:
                    events.append(current_event)
                    current_event = None
                    
        if current_event is not None:
            events.append(current_event)
            
        processed_events = []
        for ev in events:
            if ev['count'] < 3:
                continue
                
            try:
                t1 = datetime.strptime(ev['start_time'], '%Y-%m-%d %H:%M:%S')
                t2 = datetime.strptime(ev['end_time'], '%Y-%m-%d %H:%M:%S')
                duration_mins = (t2 - t1).total_seconds() / 60.0
                
                if duration_mins < 1.5:
                    continue
                    
                start_v = ev['start_voltage']
                end_v = ev['end_voltage']
                if start_v is None or end_v is None:
                    continue
                    
                v_drop = start_v - end_v
                drop_rate = (v_drop / duration_mins) * 60.0 if duration_mins > 0 else 0.0
                avg_load = sum(ev['loads']) / len(ev['loads'])
                
                is_24v = start_v > 18.0
                
                if duration_mins < 10.0:
                    health_pct = None
                    rating = "Too Short to Assess"
                else:
                    if is_24v:
                        baseline = 2.5 + (avg_load / 100.0) * 8.0
                        max_rate = 12.0
                    else:
                        baseline = 1.25 + (avg_load / 100.0) * 4.0
                        max_rate = 6.0
                        
                    if drop_rate <= baseline:
                        health_pct = 100.0
                    else:
                        health_pct = 100.0 - ((drop_rate - baseline) / (max_rate - baseline)) * 100.0
                        
                    health_pct = min(max(health_pct, 0.0), 100.0)
                    
                    if health_pct >= 90.0:
                        rating = "Excellent"
                    elif health_pct >= 75.0:
                        rating = "Good"
                    elif health_pct >= 50.0:
                        rating = "Fair"
                    else:
                        rating = "Replace Battery"
                    
                processed_events.append({
                    'date': ev['start_time'].split(' ')[0],
                    'start_time': ev['start_time'],
                    'end_time': ev['end_time'],
                    'duration_mins': f"{duration_mins:.1f}",
                    'start_voltage': f"{start_v:.2f}",
                    'end_voltage': f"{end_v:.2f}",
                    'voltage_drop': f"{v_drop:.2f}",
                    'avg_load_pct': f"{avg_load:.1f}",
                    'drop_rate_v_hr': f"{drop_rate:.2f}",
                    'health_score': "N/A" if health_pct is None else f"{health_pct:.0f}",
                    'health_rating': rating
                })
            except Exception:
                continue
                
        processed_events.reverse()
        return processed_events[:limit]
