HTML_CONTENT = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>NUT UPS Dashboard</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
    <link href="https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;500;600;700;800&display=swap" rel="stylesheet">
    <style>
        body {
            font-family: 'Outfit', sans-serif;
        }
        .glass {
            background: rgba(15, 23, 42, 0.45);
            backdrop-filter: blur(16px);
            -webkit-backdrop-filter: blur(16px);
            border: 1px solid rgba(255, 255, 255, 0.08);
        }
        @keyframes pulse-soft {
            0%, 100% { opacity: 1; transform: scale(1); }
            50% { opacity: 0.6; transform: scale(0.95); }
        }
        .animate-pulse-soft {
            animation: pulse-soft 2s infinite ease-in-out;
        }
    </style>
</head>
<body class="bg-gradient-to-br from-slate-950 via-slate-900 to-indigo-950 min-h-screen text-slate-100 p-4 md:p-8">
    <div class="max-w-7xl mx-auto space-y-6">
        
        <!-- Header -->
        <header class="glass rounded-3xl p-6 flex flex-col md:flex-row justify-between items-center gap-4">
            <div class="flex items-center gap-4">
                <div class="w-12 h-12 rounded-2xl bg-gradient-to-tr from-indigo-500 to-purple-600 flex items-center justify-center shadow-lg shadow-indigo-500/30">
                    <svg class="w-6 h-6 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 10V3L4 14h7v7l9-11h-7z" />
                    </svg>
                </div>
                <div>
                    <h1 class="text-2xl font-extrabold tracking-tight">NUT UPS Monitor</h1>
                    <p class="text-sm text-slate-400">Orange Pi Zero 3 Home Server</p>
                </div>
            </div>
            <div class="flex items-center gap-3">
                <div id="firmware-update-badge" class="hidden flex items-center gap-2 bg-indigo-500/20 border border-indigo-500/30 px-4 py-2 rounded-full cursor-pointer hover:bg-indigo-500/30 transition-all duration-300 animate-pulse-soft" onclick="scrollToFirmwareSettings()">
                    <span class="w-2 h-2 bg-indigo-400 rounded-full"></span>
                    <span class="text-xs font-semibold text-indigo-400 uppercase tracking-wider">🎁 Update Available</span>
                </div>
                
                <div class="flex items-center gap-2 bg-emerald-500/10 border border-emerald-500/20 px-4 py-2 rounded-full">
                    <span class="w-2.5 h-2.5 bg-emerald-400 rounded-full animate-ping"></span>
                    <span class="text-xs font-semibold text-emerald-400 uppercase tracking-wider">Live Monitoring Active</span>
                </div>
            </div>
        </header>

        <!-- Ambient Status Banner -->
        <section id="card-sensor-container" class="glass rounded-3xl p-6 transition-all duration-300 hover:border-indigo-500/30 space-y-4">
            <div class="flex justify-between items-center border-b border-white/5 pb-3">
                <div>
                    <h2 class="text-sm font-bold tracking-tight text-slate-200">Ambient Monitoring</h2>
                    <p class="text-[10px] text-slate-400">Jaalee JHT22 Bluetooth temperature & humidity sensors</p>
                </div>
                <div class="flex items-center gap-2 bg-indigo-500/10 border border-indigo-500/20 px-3 py-1 rounded-full">
                    <span class="w-2 h-2 bg-indigo-400 rounded-full animate-ping"></span>
                    <span class="text-[9px] font-semibold text-indigo-400 uppercase tracking-wider">BLE Scanning Active</span>
                </div>
            </div>
            
            <!-- Sensor Rows list -->
            <div id="sensor-rows-list" class="divide-y divide-white/5 space-y-3">
                <div class="text-center text-slate-500 py-2 text-xs">No BLE sensors detected yet.</div>
            </div>
        </section>

        <!-- Live UPS Cards -->
        <main class="grid md:grid-cols-2 gap-6">
            <!-- UPS 1 -->
            <section id="card-ups1" class="glass rounded-3xl p-6 space-y-6 transition-all duration-300 hover:border-indigo-500/30">
                <div class="flex justify-between items-start">
                    <div class="flex-1">
                        <div class="flex items-center gap-2 group">
                            <h2 id="ups1-title" class="text-xl font-bold tracking-tight">UPS Unit 1</h2>
                            <button onclick="startEditName('ups1')" class="opacity-0 group-hover:opacity-100 transition-opacity p-1 hover:text-indigo-400" title="Edit Name">
                                <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15.232 5.232l3.536 3.536m-2.036-5.036a2.5 2.5 0 113.536 3.536L6.5 21.036H3v-3.572L16.732 3.732z" />
                                </svg>
                            </button>
                        </div>
                        <div id="ups1-edit-container" class="hidden flex items-center gap-2 mt-1">
                            <input id="ups1-edit-input" type="text" class="bg-slate-900 border border-white/10 rounded-xl px-2 py-1 text-sm text-slate-100 focus:outline-none focus:border-indigo-500 w-full max-w-xs" />
                            <button onclick="saveName('ups1')" class="bg-indigo-600 hover:bg-indigo-700 text-white rounded-xl px-2 py-1 text-xs font-bold transition-all shadow shadow-indigo-600/20">Save</button>
                            <button onclick="cancelEditName('ups1')" class="text-slate-400 hover:text-slate-200 text-xs px-1">Cancel</button>
                        </div>
                        <p id="ups1-model" class="text-xs text-slate-400 mt-0.5">Loading device info...</p>
                        <div id="ups1-health-container" class="flex items-center gap-1.5 mt-1.5 text-xs text-slate-400">
                            <span id="ups1-health-dot" class="w-2.5 h-2.5 rounded-full bg-slate-500"></span>
                            <span id="ups1-health-text">Battery Health: Unknown (No events logged)</span>
                        </div>
                    </div>
                    <div class="flex flex-col items-end gap-2">
                        <span id="ups1-status-badge" class="px-3 py-1 rounded-full text-xs font-bold tracking-wide uppercase">Unknown</span>
                        <button id="ups1-beeper-btn" onclick="toggleBeeper('ups1')" class="flex items-center gap-1.5 px-2.5 py-1.5 rounded-xl bg-white/5 border border-white/10 hover:bg-indigo-500/20 hover:border-indigo-500/30 text-[10px] font-semibold text-slate-300 hover:text-indigo-300 transition-all" title="Toggle Alarm Beeper">
                            <svg id="ups1-beeper-icon" class="w-3.5 h-3.5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15.536 8.464a5 5 0 010 7.072M18.364 5.636a9 9 0 010 12.728M12 18.75V5.25L7.75 9.5H4.5v5h3.25L12 18.75z" />
                            </svg>
                            <span id="ups1-beeper-text">Beeper: On</span>
                        </button>
                    </div>
                </div>

                <div class="flex flex-col sm:flex-row items-center gap-6 justify-around">
                    <!-- Gauge -->
                    <div class="relative w-32 h-32 flex items-center justify-center">
                        <svg class="w-32 h-32 transform -rotate-90">
                            <circle cx="64" cy="64" r="54" class="stroke-slate-800" stroke-width="8" fill="transparent" />
                            <circle cx="64" cy="64" r="54" id="ups1-charge-ring" class="stroke-indigo-500 transition-all duration-500" stroke-width="8" fill="transparent" stroke-dasharray="339.292" stroke-dashoffset="339.292" stroke-linecap="round" />
                        </svg>
                        <div class="absolute inset-0 flex flex-col items-center justify-center">
                            <span id="ups1-charge-text" class="text-3xl font-extrabold tracking-tight">--%</span>
                            <span id="ups1-charge-label" class="text-[10px] uppercase text-slate-400 tracking-wider font-semibold mt-0.5">Battery</span>
                        </div>
                    </div>

                    <!-- Details Grid -->
                    <div class="grid grid-cols-2 gap-4 w-full sm:w-auto flex-1">
                        <div class="bg-white/5 border border-white/5 rounded-2xl p-3">
                            <span class="text-xs text-slate-400 block font-medium">Input Voltage</span>
                            <span id="ups1-input-volts" class="text-lg font-bold tracking-tight mt-1 block">-- V</span>
                        </div>
                        <div class="bg-white/5 border border-white/5 rounded-2xl p-3">
                            <span class="text-xs text-slate-400 block font-medium">Output Voltage</span>
                            <span id="ups1-out-volts" class="text-lg font-bold tracking-tight mt-1 block">-- V</span>
                        </div>
                        <div class="bg-white/5 border border-white/5 rounded-2xl p-3">
                            <span class="text-xs text-slate-400 block font-medium">Battery Voltage</span>
                            <span id="ups1-bat-volts" class="text-lg font-bold tracking-tight mt-1 block">-- V</span>
                        </div>
                        <div class="bg-white/5 border border-white/5 rounded-2xl p-3">
                            <span class="text-xs text-slate-400 block font-medium">Current Load</span>
                            <span id="ups1-load" class="text-lg font-bold tracking-tight mt-1 block">--</span>
                        </div>
                    </div>
                </div>
                
                <!-- Divider & Power Controls -->
                <div class="border-t border-white/5 pt-4 space-y-3">
                    <button onclick="toggleControlZone('ups1')" class="flex justify-between items-center w-full text-xs font-semibold uppercase tracking-wider text-slate-400 hover:text-slate-200 transition-colors">
                        <span>Power Controls</span>
                        <svg id="ups1-control-arrow" class="w-3.5 h-3.5 transform transition-transform" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7" />
                        </svg>
                    </button>
                    
                    <div id="ups1-control-zone" class="hidden grid grid-cols-2 gap-3 pt-2">
                        <!-- Direct Load Controls -->
                        <div class="col-span-2 text-[10px] uppercase font-bold tracking-wider text-slate-500 mb-0.5">Direct Outlets Control</div>
                        <button id="ups1-load-off-btn" onclick="openConfirmModal('ups1', 'off')" class="flex items-center justify-center gap-1.5 px-3 py-2 rounded-xl border border-rose-500/20 bg-rose-500/5 hover:bg-rose-500/15 text-rose-400 text-xs font-bold transition-all" title="Turn off UPS load outlets immediately">
                            <svg class="w-3.5 h-3.5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M18.364 18.364A9 9 0 005.636 5.636m12.728 12.728A9 9 0 015.636 5.636m12.728 12.728L5.636 5.636" />
                            </svg>
                            Turn Off Load
                        </button>
                        <button id="ups1-load-on-btn" onclick="openConfirmModal('ups1', 'on')" class="flex items-center justify-center gap-1.5 px-3 py-2 rounded-xl border border-emerald-500/20 bg-emerald-500/5 hover:bg-emerald-500/15 text-emerald-400 text-xs font-bold transition-all" title="Turn on UPS load outlets immediately">
                            <svg class="w-3.5 h-3.5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 10V3L4 14h7v7l9-11h-7z" />
                            </svg>
                            Turn On Load
                        </button>

                        <!-- Delayed / Return Controls -->
                        <div class="col-span-2 text-[10px] uppercase font-bold tracking-wider text-slate-500 mt-2 mb-0.5">Delayed Shutdown Commands</div>
                        <button id="ups1-shutdown-return-btn" onclick="openConfirmModal('ups1', 'shutdown_return')" class="flex items-center justify-center gap-1.5 px-3 py-2 rounded-xl border border-amber-500/20 bg-amber-500/5 hover:bg-amber-500/15 text-amber-400 text-xs font-bold transition-all" title="Shutdown load and return when power is back">
                            <svg class="w-3.5 h-3.5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 4v5h.582m15.356 2A8.001 8.001 0 1121.21 8H17" />
                            </svg>
                            Shutdown & Return
                        </button>
                        <button id="ups1-shutdown-stayoff-btn" onclick="openConfirmModal('ups1', 'shutdown_stayoff')" class="flex items-center justify-center gap-1.5 px-3 py-2 rounded-xl border border-rose-500/20 bg-rose-500/5 hover:bg-rose-500/15 text-rose-400 text-xs font-bold transition-all" title="Shutdown load and remain off">
                            <svg class="w-3.5 h-3.5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10 14l2-2m0 0l2-2m-2 2l-2-2m2 2l2 2m7-2a9 9 0 11-18 0 9 9 0 0118 0z" />
                            </svg>
                            Shutdown & Stay Off
                        </button>
                        
                        <button id="ups1-shutdown-stop-btn" onclick="openConfirmModal('ups1', 'shutdown_stop')" class="col-span-2 flex items-center justify-center gap-1.5 px-3 py-2 rounded-xl border border-indigo-500/20 bg-indigo-500/5 hover:bg-indigo-500/15 text-indigo-400 text-xs font-bold transition-all" title="Cancel a shutdown in progress">
                            <svg class="w-3.5 h-3.5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10 9v6m4-6v6m7-3a9 9 0 11-18 0 9 9 0 0118 0z" />
                            </svg>
                            Cancel Shutdown Sequence
                        </button>

                        <!-- Configuration Settings -->
                        <div class="col-span-2 text-[10px] uppercase font-bold tracking-wider text-slate-500 mt-2 mb-0.5">Configuration Settings</div>
                        <div class="col-span-2 space-y-3">
                            <div class="flex items-center justify-between gap-3 bg-white/5 border border-white/5 rounded-2xl p-3">
                                <div>
                                    <span class="text-xs font-semibold block text-slate-300">Shutdown Delay</span>
                                    <span class="text-[10px] text-slate-400">Seconds to wait before load cut (12-540)</span>
                                </div>
                                <div class="flex items-center gap-2">
                                    <input id="ups1-delay-shutdown-input" type="number" min="12" max="540" class="bg-slate-900 border border-white/10 rounded-xl px-2 py-1 text-sm text-slate-100 focus:outline-none focus:border-indigo-500 w-24 text-center" />
                                    <button id="ups1-delay-shutdown-btn" onclick="saveShutdownDelay('ups1')" class="bg-indigo-600 hover:bg-indigo-700 disabled:opacity-50 text-white rounded-xl px-3 py-1 text-xs font-bold transition-all shadow shadow-indigo-600/20">Apply</button>
                                </div>
                            </div>
                            <div class="flex items-center justify-between gap-3 bg-white/5 border border-white/5 rounded-2xl p-3">
                                <div>
                                    <span class="text-xs font-semibold block text-slate-300">Startup Delay</span>
                                    <span class="text-[10px] text-slate-400">Seconds to wait before restart (60-599940)</span>
                                </div>
                                <div class="flex items-center gap-2">
                                    <input id="ups1-delay-start-input" type="number" min="60" max="599940" class="bg-slate-900 border border-white/10 rounded-xl px-2 py-1 text-sm text-slate-100 focus:outline-none focus:border-indigo-500 w-24 text-center" />
                                    <button id="ups1-delay-start-btn" onclick="saveStartupDelay('ups1')" class="bg-indigo-600 hover:bg-indigo-700 disabled:opacity-50 text-white rounded-xl px-3 py-1 text-xs font-bold transition-all shadow shadow-indigo-600/20">Apply</button>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </section>

            <!-- UPS 2 -->
            <section id="card-ups2" class="glass rounded-3xl p-6 space-y-6 transition-all duration-300 hover:border-indigo-500/30">
                <div class="flex justify-between items-start">
                    <div class="flex-1">
                        <div class="flex items-center gap-2 group">
                            <h2 id="ups2-title" class="text-xl font-bold tracking-tight">UPS Unit 2</h2>
                            <button onclick="startEditName('ups2')" class="opacity-0 group-hover:opacity-100 transition-opacity p-1 hover:text-indigo-400" title="Edit Name">
                                <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15.232 5.232l3.536 3.536m-2.036-5.036a2.5 2.5 0 113.536 3.536L6.5 21.036H3v-3.572L16.732 3.732z" />
                                </svg>
                            </button>
                        </div>
                        <div id="ups2-edit-container" class="hidden flex items-center gap-2 mt-1">
                            <input id="ups2-edit-input" type="text" class="bg-slate-900 border border-white/10 rounded-xl px-2 py-1 text-sm text-slate-100 focus:outline-none focus:border-indigo-500 w-full max-w-xs" />
                            <button onclick="saveName('ups2')" class="bg-indigo-600 hover:bg-indigo-700 text-white rounded-xl px-2 py-1 text-xs font-bold transition-all shadow shadow-indigo-600/20">Save</button>
                            <button onclick="cancelEditName('ups2')" class="text-slate-400 hover:text-slate-200 text-xs px-1">Cancel</button>
                        </div>
                        <p id="ups2-model" class="text-xs text-slate-400 mt-0.5">Loading device info...</p>
                        <div id="ups2-health-container" class="flex items-center gap-1.5 mt-1.5 text-xs text-slate-400">
                            <span id="ups2-health-dot" class="w-2.5 h-2.5 rounded-full bg-slate-500"></span>
                            <span id="ups2-health-text">Battery Health: Unknown (No events logged)</span>
                        </div>
                    </div>
                    <div class="flex flex-col items-end gap-2">
                        <span id="ups2-status-badge" class="px-3 py-1 rounded-full text-xs font-bold tracking-wide uppercase">Unknown</span>
                        <button id="ups2-beeper-btn" onclick="toggleBeeper('ups2')" class="flex items-center gap-1.5 px-2.5 py-1.5 rounded-xl bg-white/5 border border-white/10 hover:bg-indigo-500/20 hover:border-indigo-500/30 text-[10px] font-semibold text-slate-300 hover:text-indigo-300 transition-all" title="Toggle Alarm Beeper">
                            <svg id="ups2-beeper-icon" class="w-3.5 h-3.5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15.536 8.464a5 5 0 010 7.072M18.364 5.636a9 9 0 010 12.728M12 18.75V5.25L7.75 9.5H4.5v5h3.25L12 18.75z" />
                            </svg>
                            <span id="ups2-beeper-text">Beeper: On</span>
                        </button>
                    </div>
                </div>

                <div class="flex flex-col sm:flex-row items-center gap-6 justify-around">
                    <!-- Gauge -->
                    <div class="relative w-32 h-32 flex items-center justify-center">
                        <svg class="w-32 h-32 transform -rotate-90">
                            <circle cx="64" cy="64" r="54" class="stroke-slate-800" stroke-width="8" fill="transparent" />
                            <circle cx="64" cy="64" r="54" id="ups2-charge-ring" class="stroke-indigo-500 transition-all duration-500" stroke-width="8" fill="transparent" stroke-dasharray="339.292" stroke-dashoffset="339.292" stroke-linecap="round" />
                        </svg>
                        <div class="absolute inset-0 flex flex-col items-center justify-center">
                            <span id="ups2-charge-text" class="text-3xl font-extrabold tracking-tight">--%</span>
                            <span id="ups2-charge-label" class="text-[10px] uppercase text-slate-400 tracking-wider font-semibold mt-0.5">Battery</span>
                        </div>
                    </div>

                    <!-- Details Grid -->
                    <div class="grid grid-cols-2 gap-4 w-full sm:w-auto flex-1">
                        <div class="bg-white/5 border border-white/5 rounded-2xl p-3">
                            <span class="text-xs text-slate-400 block font-medium">Input Voltage</span>
                            <span id="ups2-input-volts" class="text-lg font-bold tracking-tight mt-1 block">-- V</span>
                        </div>
                        <div class="bg-white/5 border border-white/5 rounded-2xl p-3">
                            <span class="text-xs text-slate-400 block font-medium">Output Voltage</span>
                            <span id="ups2-out-volts" class="text-lg font-bold tracking-tight mt-1 block">-- V</span>
                        </div>
                        <div class="bg-white/5 border border-white/5 rounded-2xl p-3">
                            <span class="text-xs text-slate-400 block font-medium">Battery Voltage</span>
                            <span id="ups2-bat-volts" class="text-lg font-bold tracking-tight mt-1 block">-- V</span>
                        </div>
                        <div class="bg-white/5 border border-white/5 rounded-2xl p-3">
                            <span class="text-xs text-slate-400 block font-medium">Current Load</span>
                            <span id="ups2-load" class="text-lg font-bold tracking-tight mt-1 block">--</span>
                        </div>
                    </div>
                </div>
                
                <!-- Divider & Power Controls -->
                <div class="border-t border-white/5 pt-4 space-y-3">
                    <button onclick="toggleControlZone('ups2')" class="flex justify-between items-center w-full text-xs font-semibold uppercase tracking-wider text-slate-400 hover:text-slate-200 transition-colors">
                        <span>Power Controls</span>
                        <svg id="ups2-control-arrow" class="w-3.5 h-3.5 transform transition-transform" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7" />
                        </svg>
                    </button>
                    
                    <div id="ups2-control-zone" class="hidden grid grid-cols-2 gap-3 pt-2">
                        <!-- Direct Load Controls -->
                        <div class="col-span-2 text-[10px] uppercase font-bold tracking-wider text-slate-500 mb-0.5">Direct Outlets Control</div>
                        <button id="ups2-load-off-btn" onclick="openConfirmModal('ups2', 'off')" class="flex items-center justify-center gap-1.5 px-3 py-2 rounded-xl border border-rose-500/20 bg-rose-500/5 hover:bg-rose-500/15 text-rose-400 text-xs font-bold transition-all" title="Turn off UPS load outlets immediately">
                            <svg class="w-3.5 h-3.5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M18.364 18.364A9 9 0 005.636 5.636m12.728 12.728A9 9 0 015.636 5.636m12.728 12.728L5.636 5.636" />
                            </svg>
                            Turn Off Load
                        </button>
                        <button id="ups2-load-on-btn" onclick="openConfirmModal('ups2', 'on')" class="flex items-center justify-center gap-1.5 px-3 py-2 rounded-xl border border-emerald-500/20 bg-emerald-500/5 hover:bg-emerald-500/15 text-emerald-400 text-xs font-bold transition-all" title="Turn on UPS load outlets immediately">
                            <svg class="w-3.5 h-3.5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 10V3L4 14h7v7l9-11h-7z" />
                            </svg>
                            Turn On Load
                        </button>

                        <!-- Delayed / Return Controls -->
                        <div class="col-span-2 text-[10px] uppercase font-bold tracking-wider text-slate-500 mt-2 mb-0.5">Delayed Shutdown Commands</div>
                        <button id="ups2-shutdown-return-btn" onclick="openConfirmModal('ups2', 'shutdown_return')" class="flex items-center justify-center gap-1.5 px-3 py-2 rounded-xl border border-amber-500/20 bg-amber-500/5 hover:bg-amber-500/15 text-amber-400 text-xs font-bold transition-all" title="Shutdown load and return when power is back">
                            <svg class="w-3.5 h-3.5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 4v5h.582m15.356 2A8.001 8.001 0 1121.21 8H17" />
                            </svg>
                            Shutdown & Return
                        </button>
                        <button id="ups2-shutdown-stayoff-btn" onclick="openConfirmModal('ups2', 'shutdown_stayoff')" class="flex items-center justify-center gap-1.5 px-3 py-2 rounded-xl border border-rose-500/20 bg-rose-500/5 hover:bg-rose-500/15 text-rose-400 text-xs font-bold transition-all" title="Shutdown load and remain off">
                            <svg class="w-3.5 h-3.5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10 14l2-2m0 0l2-2m-2 2l-2-2m2 2l2 2m7-2a9 9 0 11-18 0 9 9 0 0118 0z" />
                            </svg>
                            Shutdown & Stay Off
                        </button>
                        
                        <button id="ups2-shutdown-stop-btn" onclick="openConfirmModal('ups2', 'shutdown_stop')" class="col-span-2 flex items-center justify-center gap-1.5 px-3 py-2 rounded-xl border border-indigo-500/20 bg-indigo-500/5 hover:bg-indigo-500/15 text-indigo-400 text-xs font-bold transition-all" title="Cancel a shutdown in progress">
                            <svg class="w-3.5 h-3.5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10 9v6m4-6v6m7-3a9 9 0 11-18 0 9 9 0 0118 0z" />
                            </svg>
                            Cancel Shutdown Sequence
                        </button>

                        <!-- Configuration Settings -->
                        <div class="col-span-2 text-[10px] uppercase font-bold tracking-wider text-slate-500 mt-2 mb-0.5">Configuration Settings</div>
                        <div class="col-span-2 space-y-3">
                            <div class="flex items-center justify-between gap-3 bg-white/5 border border-white/5 rounded-2xl p-3">
                                <div>
                                    <span class="text-xs font-semibold block text-slate-300">Shutdown Delay</span>
                                    <span class="text-[10px] text-slate-400">Seconds to wait before load cut (12-540)</span>
                                </div>
                                <div class="flex items-center gap-2">
                                    <input id="ups2-delay-shutdown-input" type="number" min="12" max="540" class="bg-slate-900 border border-white/10 rounded-xl px-2 py-1 text-sm text-slate-100 focus:outline-none focus:border-indigo-500 w-24 text-center" />
                                    <button id="ups2-delay-shutdown-btn" onclick="saveShutdownDelay('ups2')" class="bg-indigo-600 hover:bg-indigo-700 disabled:opacity-50 text-white rounded-xl px-3 py-1 text-xs font-bold transition-all shadow shadow-indigo-600/20">Apply</button>
                                </div>
                            </div>
                            <div class="flex items-center justify-between gap-3 bg-white/5 border border-white/5 rounded-2xl p-3">
                                <div>
                                    <span class="text-xs font-semibold block text-slate-300">Startup Delay</span>
                                    <span class="text-[10px] text-slate-400">Seconds to wait before restart (60-599940)</span>
                                </div>
                                <div class="flex items-center gap-2">
                                    <input id="ups2-delay-start-input" type="number" min="60" max="599940" class="bg-slate-900 border border-white/10 rounded-xl px-2 py-1 text-sm text-slate-100 focus:outline-none focus:border-indigo-500 w-24 text-center" />
                                    <button id="ups2-delay-start-btn" onclick="saveStartupDelay('ups2')" class="bg-indigo-600 hover:bg-indigo-700 disabled:opacity-50 text-white rounded-xl px-3 py-1 text-xs font-bold transition-all shadow shadow-indigo-600/20">Apply</button>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </section>
        </main>

        <!-- History Chart Section -->
        <section class="glass rounded-3xl p-6 space-y-6">
            <div class="flex flex-col lg:flex-row justify-between items-start lg:items-center gap-4">
                <div>
                    <h2 class="text-xl font-bold tracking-tight">Historical Logs</h2>
                    <p class="text-xs text-slate-400 mt-0.5">Data retrieved from USB log files</p>
                </div>
                <div class="flex flex-wrap items-center gap-3">
                    <!-- UPS Selector -->
                    <div class="flex bg-slate-900 border border-white/10 rounded-xl p-1 shadow-inner">
                        <button id="btn-chart-ups1" onclick="selectChartUPS('ups1')" class="px-4 py-2 text-xs font-bold rounded-lg transition-all bg-indigo-500 text-white shadow shadow-indigo-500/20">UPS 1</button>
                        <button id="btn-chart-ups2" onclick="selectChartUPS('ups2')" class="px-4 py-2 text-xs font-bold rounded-lg transition-all text-slate-400 hover:text-white">UPS 2</button>
                    </div>
                    <!-- Time Range Selector -->
                    <div class="flex bg-slate-900 border border-white/10 rounded-xl p-1 shadow-inner">
                        <button id="btn-range-1h" onclick="selectTimeRange('1h')" class="px-3 py-2 text-xs font-bold rounded-lg transition-all text-slate-400 hover:text-white">1h</button>
                        <button id="btn-range-6h" onclick="selectTimeRange('6h')" class="px-3 py-2 text-xs font-bold rounded-lg transition-all text-slate-400 hover:text-white">6h</button>
                        <button id="btn-range-12h" onclick="selectTimeRange('12h')" class="px-3 py-2 text-xs font-bold rounded-lg transition-all text-slate-400 hover:text-white">12h</button>
                        <button id="btn-range-24h" onclick="selectTimeRange('24h')" class="px-3 py-2 text-xs font-bold rounded-lg transition-all bg-indigo-500 text-white shadow shadow-indigo-500/20">24h</button>
                    </div>
                </div>
            </div>

            <!-- Charts Container -->
            <div class="grid md:grid-cols-2 gap-6">
                <div class="bg-slate-950/40 border border-white/5 p-4 rounded-2xl h-80 flex flex-col justify-between">
                    <h3 class="text-xs uppercase text-slate-400 font-semibold tracking-wider mb-2">Battery Charge History (%)</h3>
                    <div class="flex-1 relative">
                        <canvas id="chart-charge"></canvas>
                    </div>
                </div>
                <div class="bg-slate-950/40 border border-white/5 p-4 rounded-2xl h-80 flex flex-col justify-between">
                    <h3 class="text-xs uppercase text-slate-400 font-semibold tracking-wider mb-2">Voltages History (V)</h3>
                    <div class="flex-1 relative">
                        <canvas id="chart-voltage"></canvas>
                    </div>
                </div>
            </div>
        </section>

        <!-- Battery Health Section -->
        <section class="glass rounded-3xl p-6 space-y-6">
            <div>
                <h2 class="text-xl font-bold tracking-tight">Battery Health & Outage History</h2>
                <p class="text-xs text-slate-400 mt-0.5">Passive health analysis derived from log discharge events</p>
            </div>
            
            <div class="grid md:grid-cols-2 gap-6">
                <!-- UPS 1 Health -->
                <div class="bg-slate-950/40 border border-white/5 p-4 rounded-2xl flex flex-col justify-between">
                    <h3 id="health-ups1-title" class="text-xs uppercase text-slate-400 font-semibold tracking-wider mb-3">UPS Unit 1 Health Events</h3>
                    <div class="overflow-x-auto">
                        <table class="w-full text-left text-xs text-slate-300">
                            <thead>
                                <tr class="border-b border-white/10 text-slate-400 uppercase tracking-wider font-semibold text-[10px]">
                                    <th class="py-2">Date</th>
                                    <th class="py-2">Duration</th>
                                    <th class="py-2">Voltage Span</th>
                                    <th class="py-2">Decline Rate</th>
                                    <th class="py-2 text-right">Est. Health</th>
                                </tr>
                            </thead>
                            <tbody id="health-table-ups1">
                                <tr>
                                    <td colspan="5" class="py-4 text-center text-slate-500">No discharge events recorded yet.</td>
                                </tr>
                            </tbody>
                        </table>
                    </div>
                </div>
                
                <!-- UPS 2 Health -->
                <div class="bg-slate-950/40 border border-white/5 p-4 rounded-2xl flex flex-col justify-between">
                    <h3 id="health-ups2-title" class="text-xs uppercase text-slate-400 font-semibold tracking-wider mb-3">UPS Unit 2 Health Events</h3>
                    <div class="overflow-x-auto">
                        <table class="w-full text-left text-xs text-slate-300">
                            <thead>
                                <tr class="border-b border-white/10 text-slate-400 uppercase tracking-wider font-semibold text-[10px]">
                                    <th class="py-2">Date</th>
                                    <th class="py-2">Duration</th>
                                    <th class="py-2">Voltage Span</th>
                                    <th class="py-2">Decline Rate</th>
                                    <th class="py-2 text-right">Est. Health</th>
                                </tr>
                            </thead>
                            <tbody id="health-table-ups2">
                                <tr>
                                    <td colspan="5" class="py-4 text-center text-slate-500">No discharge events recorded yet.</td>
                                </tr>
                            </tbody>
                        </table>
                    </div>
                </div>
            </div>
        </section>

        <!-- System & Firmware Section -->
        <section id="section-firmware" class="glass rounded-3xl p-6 space-y-6">
            <div>
                <h2 class="text-xl font-bold tracking-tight">System Settings & Firmware</h2>
                <p class="text-xs text-slate-400 mt-0.5">Manage dashboard system updates and version control</p>
            </div>
            
            <div class="grid md:grid-cols-2 gap-6">
                <!-- Firmware Info & Update Panel -->
                <div class="bg-slate-950/40 border border-white/5 p-4 rounded-2xl space-y-4">
                    <div class="flex items-center justify-between">
                        <div>
                            <span class="text-xs uppercase text-slate-400 font-semibold tracking-wider block">Dashboard Version</span>
                            <span id="current-version-display" class="text-sm font-bold text-slate-200">v0.1</span>
                        </div>
                        <button id="btn-check-updates" onclick="checkForUpdates()" class="flex items-center gap-1.5 px-3 py-1.5 rounded-xl bg-indigo-600 hover:bg-indigo-700 text-xs font-bold text-white transition-all shadow shadow-indigo-600/20">
                            Check for Updates
                        </button>
                    </div>
                    
                    <div id="update-status-container" class="hidden text-xs space-y-2 p-3 bg-white/5 border border-white/5 rounded-xl">
                        <div class="flex items-center justify-between">
                            <span id="update-status-text" class="font-medium text-slate-300">Checking...</span>
                            <span id="update-available-badge" class="hidden px-2 py-0.5 rounded-full text-[9px] font-bold bg-indigo-500/20 text-indigo-400 border border-indigo-500/30">UPDATE AVAILABLE</span>
                        </div>
                        <div id="version-selector-container" class="hidden flex flex-col gap-2 pt-2 border-t border-white/5">
                            <label for="version-select" class="text-[10px] text-slate-400 font-medium">Select target version to install (upgrade/downgrade):</label>
                            <div class="flex items-center gap-2">
                                <select id="version-select" class="flex-1 bg-slate-900 border border-white/10 rounded-xl px-2 py-1.5 text-xs text-slate-200 focus:outline-none focus:border-indigo-500">
                                    <!-- Populated dynamically -->
                                </select>
                                <button id="btn-install-version" onclick="installSelectedVersion()" class="bg-purple-600 hover:bg-purple-700 text-white rounded-xl px-3 py-1.5 text-xs font-bold transition-all shadow shadow-purple-600/20">
                                    Install
                                </button>
                            </div>
                        </div>
                    </div>
                </div>

                <!-- Update Progress & Log -->
                <div id="update-progress-card" class="hidden bg-slate-950/40 border border-white/5 p-4 rounded-2xl flex flex-col justify-between space-y-4">
                    <div>
                        <span class="text-xs uppercase text-slate-400 font-semibold tracking-wider block mb-1">Update Progress</span>
                        <div class="w-full bg-slate-900 rounded-full h-2 overflow-hidden border border-white/10 mt-2">
                            <div id="update-progress-bar" class="bg-indigo-500 h-full rounded-full transition-all duration-300" style="width: 0%"></div>
                        </div>
                    </div>
                    <div id="update-log" class="bg-slate-900/60 rounded-xl p-3 border border-white/5 text-[10px] font-mono h-24 overflow-y-auto space-y-1 text-slate-400">
                        <!-- Progress log entries -->
                    </div>
                </div>
            </div>
        </section>
    </div>

    <script>
        let currentChartUPS = 'ups1';
        let chargeChart = null;
        let voltageChart = null;
        let rawHistoryData = {};
        let isEditing = { ups1: false, ups2: false };
        let customNames = { ups1: 'UPS Unit 1', ups2: 'UPS Unit 2' };

        function startEditName(id) {
            isEditing[id] = true;
            document.getElementById(`${id}-edit-container`).classList.remove('hidden');
            document.getElementById(`${id}-edit-input`).value = customNames[id];
            document.getElementById(`${id}-edit-input`).focus();
        }

        function cancelEditName(id) {
            isEditing[id] = false;
            document.getElementById(`${id}-edit-container`).classList.add('hidden');
        }

        async function saveName(id) {
            const input = document.getElementById(`${id}-edit-input`);
            const newName = input.value.trim();
            if (!newName) return;

            try {
                const payload = {};
                payload[`${id}_name`] = newName;
                
                const res = await fetch('/api/config', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify(payload)
                });
                
                if (res.ok) {
                    customNames[id] = newName;
                    document.getElementById(`${id}-title`).innerText = newName;
                    
                    const btn = document.getElementById(`btn-chart-${id}`);
                    if (btn) {
                        btn.innerText = newName;
                    }
                    
                    if (chargeChart && currentChartUPS === id) {
                        chargeChart.data.datasets[0].label = `${newName} Charge (%)`;
                        chargeChart.update();
                    }
                    if (voltageChart && currentChartUPS === id) {
                        voltageChart.data.datasets[0].label = `${newName} Battery Voltage`;
                        voltageChart.update();
                    }
                    
                    const healthTitle = document.getElementById(`health-${id}-title`);
                    if (healthTitle) {
                        healthTitle.innerText = `${newName} Health Events`;
                    }

                    cancelEditName(id);
                } else {
                    console.error("Failed to save name");
                }
            } catch (err) {
                console.error("Error saving name:", err);
            }
        }

        function setRingProgress(ringId, textId, labelId, pct, isEstimated) {
            const ring = document.getElementById(ringId);
            const text = document.getElementById(textId);
            const label = document.getElementById(labelId);
            if (!ring || !text) return;
            
            const r = 54;
            const circ = 2 * Math.PI * r;
            
            if (isNaN(pct) || pct === null || pct === undefined) {
                ring.style.strokeDashoffset = circ;
                text.innerText = '--%';
                return;
            }

            pct = Math.min(Math.max(pct, 0), 100);
            const offset = circ - (pct / 100) * circ;
            ring.style.strokeDashoffset = offset;
            text.innerText = `${Math.round(pct)}%`;
            
            if (label) {
                label.innerText = isEstimated ? 'Battery (Est)' : 'Battery';
            }

            // Change colors dynamically
            ring.className.baseVal = '';
            if (pct > 50) {
                ring.classList.add('stroke-emerald-500', 'transition-all', 'duration-500');
            } else if (pct > 20) {
                ring.classList.add('stroke-amber-500', 'transition-all', 'duration-500');
            } else {
                ring.classList.add('stroke-rose-500', 'transition-all', 'duration-500', 'animate-pulse-soft');
            }
        }

        function updateStatusBadge(badgeId, statusStr) {
            const badge = document.getElementById(badgeId);
            if (!badge) return;

            badge.innerText = statusStr || 'UNKNOWN';
            badge.className = 'px-3 py-1 rounded-full text-xs font-bold tracking-wide uppercase ';

            if (!statusStr) {
                badge.classList.add('bg-slate-800', 'text-slate-400');
                return;
            }

            if (statusStr.includes('OL')) {
                badge.classList.add('bg-emerald-500/10', 'text-emerald-400', 'border', 'border-emerald-500/20');
                badge.innerText = 'ONLINE';
            } else if (statusStr.includes('OB')) {
                badge.classList.add('bg-rose-500/10', 'text-rose-400', 'border', 'border-rose-500/20', 'animate-pulse');
                badge.innerText = 'ON BATTERY';
            } else if (statusStr.includes('LB')) {
                badge.classList.add('bg-rose-600', 'text-white', 'animate-bounce');
                badge.innerText = 'CRITICAL LOW BAT';
            } else {
                badge.classList.add('bg-amber-500/10', 'text-amber-400', 'border', 'border-amber-500/20');
            }
        }

        let activeSensorEditMac = null;
        let sensorNames = {};

        function formatRelativeTime(epochSecs) {
            if (!epochSecs) return 'Never';
            const now = Math.floor(Date.now() / 1000);
            const diff = now - epochSecs;
            if (diff < 10) return 'Just now';
            if (diff < 60) return `${diff}s ago`;
            const mins = Math.floor(diff / 60);
            if (mins < 60) return `${mins}m ago`;
            const hours = Math.floor(mins / 60);
            return `${hours}h ago`;
        }

        function getBatterySVG(pct) {
            let fillRect = '';
            if (pct > 75) {
                fillRect = '<rect x="5" y="9" width="10" height="6" fill="currentColor" />';
            } else if (pct > 30) {
                fillRect = '<rect x="5" y="9" width="6" height="6" fill="currentColor" />';
            } else {
                fillRect = '<rect x="5" y="9" width="3" height="6" fill="currentColor" />';
            }
            return `
                <rect x="2" y="6" width="16" height="12" rx="2" stroke-width="2" stroke="currentColor" fill="none" />
                <path d="M20 10v4" stroke-width="2" stroke="currentColor" stroke-linecap="round" />
                ${fillRect}
            `;
        }

        function getBatteryColorClass(pct) {
            if (pct > 75) return 'text-emerald-400';
            if (pct > 30) return 'text-amber-400';
            return 'text-rose-500 animate-pulse';
        }

        function startEditSensorName(mac) {
            activeSensorEditMac = mac;
            document.getElementById(`sensor-${mac}-edit-container`).classList.remove('hidden');
            document.getElementById(`sensor-${mac}-edit-input`).value = sensorNames[mac];
            document.getElementById(`sensor-${mac}-edit-input`).focus();
        }

        function cancelEditSensorName(mac) {
            activeSensorEditMac = null;
            document.getElementById(`sensor-${mac}-edit-container`).classList.add('hidden');
        }

        async function saveSensorName(mac) {
            const input = document.getElementById(`sensor-${mac}-edit-input`);
            const newName = input.value.trim();
            if (!newName) return;

            try {
                const payload = {};
                payload[`sensor_${mac}_name`] = newName;
                
                const res = await fetch('/api/config', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify(payload)
                });
                
                if (res.ok) {
                    sensorNames[mac] = newName;
                    document.getElementById(`sensor-${mac}-title`).innerText = newName;
                    cancelEditSensorName(mac);
                } else {
                    console.error("Failed to save sensor name");
                }
            } catch (err) {
                console.error("Error saving sensor name:", err);
            }
        }

        async function fetchStatus() {
            try {
                const res = await fetch('/api/status');
                const data = await res.json();
                
                ['ups1', 'ups2'].forEach(id => {
                    const ups = data[id];
                    const card = document.getElementById(`card-${id}`);

                    const displayName = ups['display_name'] || (id === 'ups1' ? 'UPS Unit 1' : 'UPS Unit 2');
                    customNames[id] = displayName;
                    if (!isEditing[id]) {
                        document.getElementById(`${id}-title`).innerText = displayName;
                    }
                    const btn = document.getElementById(`btn-chart-${id}`);
                    if (btn) {
                        btn.innerText = displayName;
                    }

                    if (ups.error) {
                        document.getElementById(`${id}-model`).innerText = ups.error;
                        document.getElementById(`${id}-input-volts`).innerText = '--';
                        document.getElementById(`${id}-out-volts`).innerText = '--';
                        document.getElementById(`${id}-bat-volts`).innerText = '--';
                        document.getElementById(`${id}-load`).innerText = '--';
                        setRingProgress(`${id}-charge-ring`, `${id}-charge-text`, `${id}-charge-label`, null, false);
                        updateStatusBadge(`${id}-status-badge`, 'OFFLINE');
                        
                        // Disable beeper controls on error
                        const beeperBtn = document.getElementById(`${id}-beeper-btn`);
                        const beeperText = document.getElementById(`${id}-beeper-text`);
                        const beeperIcon = document.getElementById(`${id}-beeper-icon`);
                        if (beeperBtn && beeperText && beeperIcon) {
                            beeperBtn.disabled = true;
                            beeperBtn.classList.add('opacity-50', 'cursor-not-allowed');
                            beeperText.innerText = 'Beeper: N/A';
                            beeperIcon.innerHTML = `<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5.586 15H4a1 1 0 01-1-1v-4a1 1 0 011-1h1.586l4.707-4.707C10.923 3.663 12 4.109 12 5v14c0 .891-1.077 1.337-1.707.707L5.586 15zm9.9-7.9l5.656 5.656M21.142 7.1L15.486 12.76" />`;
                        }
                        
                        // Disable all load control and shutdown buttons
                        const btnIds = ['load-off-btn', 'load-on-btn', 'shutdown-return-btn', 'shutdown-stayoff-btn', 'shutdown-stop-btn', 'delay-shutdown-btn', 'delay-start-btn'];
                        btnIds.forEach(btnId => {
                            const btn = document.getElementById(`${id}-${btnId}`);
                            if (btn) {
                                btn.disabled = true;
                                btn.classList.add('opacity-40', 'cursor-not-allowed');
                            }
                        });
                        const delayInput = document.getElementById(`${id}-delay-shutdown-input`);
                        if (delayInput) delayInput.disabled = true;
                        const startInput = document.getElementById(`${id}-delay-start-input`);
                        if (startInput) startInput.disabled = true;
                        
                        card.classList.add('opacity-60');
                        return;
                    }

                    card.classList.remove('opacity-60');
                    document.getElementById(`${id}-model`).innerText = `${ups['device.mfr'] || 'Generic'} ${ups['device.model'] || 'Voltronic/QX Device'}`;
                    document.getElementById(`${id}-input-volts`).innerText = ups['input.voltage'] ? `${ups['input.voltage']} V` : 'N/A';
                    document.getElementById(`${id}-out-volts`).innerText = ups['output.voltage'] ? `${ups['output.voltage']} V` : 'N/A';
                    document.getElementById(`${id}-bat-volts`).innerText = ups['battery.voltage'] ? `${ups['battery.voltage']} V` : 'N/A';
                    
                    // Load and calculated power draw in Watts
                    const loadVal = ups['ups.load'];
                    const realPowerNominalVal = ups['ups.realpower.nominal'];
                    let loadText = 'N/A';
                    if (loadVal && loadVal !== 'NA') {
                        const loadPct = parseFloat(loadVal);
                        if (!isNaN(loadPct)) {
                            if (realPowerNominalVal && realPowerNominalVal !== 'NA') {
                                const nomW = parseFloat(realPowerNominalVal);
                                if (!isNaN(nomW)) {
                                    if (loadPct === 0) {
                                        const minW = Math.round(0.05 * nomW);
                                        loadText = `0% (< ${minW} W)`;
                                    } else {
                                        const watts = (loadPct / 100) * nomW;
                                        loadText = `${loadPct}% (${Math.round(watts)} W)`;
                                    }
                                } else {
                                    loadText = `${loadPct}%`;
                                }
                            } else {
                                loadText = `${loadPct}%`;
                            }
                        }
                    }
                    document.getElementById(`${id}-load`).innerText = loadText;

                    
                    const pct = ups['battery.charge'] ? parseFloat(ups['battery.charge']) : null;
                    const isEstimated = ups['battery.charge.estimated'] === 'true';
                    setRingProgress(`${id}-charge-ring`, `${id}-charge-text`, `${id}-charge-label`, pct, isEstimated);
                    updateStatusBadge(`${id}-status-badge`, ups['ups.status']);

                    // Update beeper controls
                    const beeperBtn = document.getElementById(`${id}-beeper-btn`);
                    const beeperText = document.getElementById(`${id}-beeper-text`);
                    const beeperIcon = document.getElementById(`${id}-beeper-icon`);
                    if (beeperBtn && beeperText && beeperIcon) {
                        if (!ups['ups.beeper.status']) {
                            beeperBtn.disabled = true;
                            beeperBtn.classList.add('opacity-50', 'cursor-not-allowed');
                            beeperText.innerText = 'Beeper: N/A';
                            beeperIcon.innerHTML = `<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5.586 15H4a1 1 0 01-1-1v-4a1 1 0 011-1h1.586l4.707-4.707C10.923 3.663 12 4.109 12 5v14c0 .891-1.077 1.337-1.707.707L5.586 15zm9.9-7.9l5.656 5.656M21.142 7.1L15.486 12.76" />`;
                        } else {
                            beeperBtn.disabled = false;
                            beeperBtn.classList.remove('opacity-50', 'cursor-not-allowed');
                            const isEnabled = ups['ups.beeper.status'] === 'enabled';
                            beeperText.innerText = isEnabled ? 'Beeper: On' : 'Beeper: Off';
                            if (isEnabled) {
                                beeperBtn.classList.remove('border-rose-500/20', 'bg-rose-500/10', 'text-rose-400');
                                beeperBtn.classList.add('border-white/10', 'bg-white/5', 'text-slate-300');
                                beeperIcon.innerHTML = `<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15.536 8.464a5 5 0 010 7.072M18.364 5.636a9 9 0 010 12.728M12 18.75V5.25L7.75 9.5H4.5v5h3.25L12 18.75z" />`;
                            } else {
                                beeperBtn.classList.remove('border-white/10', 'bg-white/5', 'text-slate-300');
                                beeperBtn.classList.add('border-rose-500/20', 'bg-rose-500/10', 'text-rose-400');
                                beeperIcon.innerHTML = `<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5.586 15H4a1 1 0 01-1-1v-4a1 1 0 011-1h1.586l4.707-4.707C10.923 3.663 12 4.109 12 5v14c0 .891-1.077 1.337-1.707.707L5.586 15zm9.9-7.9l5.656 5.656M21.142 7.1L15.486 12.76" />`;
                            }
                        }
                    }

                    // Update all load control and shutdown buttons
                    const btnIds = ['load-off-btn', 'load-on-btn', 'shutdown-return-btn', 'shutdown-stayoff-btn', 'shutdown-stop-btn', 'delay-shutdown-btn', 'delay-start-btn'];
                    btnIds.forEach(btnId => {
                        const btn = document.getElementById(`${id}-${btnId}`);
                        if (btn) {
                            btn.disabled = false;
                            btn.classList.remove('opacity-40', 'cursor-not-allowed');
                        }
                    });
                    const delayInput = document.getElementById(`${id}-delay-shutdown-input`);
                    if (delayInput) {
                        delayInput.disabled = false;
                        if (document.activeElement !== delayInput) {
                            delayInput.value = ups['ups.delay.shutdown'] || '';
                        }
                    }
                    const startInput = document.getElementById(`${id}-delay-start-input`);
                    if (startInput) {
                        startInput.disabled = false;
                        if (document.activeElement !== startInput) {
                            startInput.value = ups['ups.delay.start'] || '';
                        }
                    }
                });

                // Parse Ambient Sensors
                const sensors = data['ambient_sensors'] || [];
                const rowsContainer = document.getElementById('sensor-rows-list');
                
                if (sensors.length === 0) {
                    rowsContainer.innerHTML = '<div class="text-center text-slate-500 py-2 text-xs">No BLE sensors detected yet.</div>';
                } else {
                    if (rowsContainer.querySelector('.text-slate-500')) {
                        rowsContainer.innerHTML = '';
                    }
                    
                    sensors.forEach(sensor => {
                        const mac = sensor.mac;
                        sensorNames[mac] = sensor.display_name;
                        
                        let row = document.getElementById(`sensor-row-${mac}`);
                        if (!row) {
                            row = document.createElement('div');
                            row.id = `sensor-row-${mac}`;
                            row.className = 'flex flex-col md:flex-row justify-between items-center gap-4 pt-3 first:pt-0';
                            row.innerHTML = `
                                <!-- Left: Name and MAC -->
                                <div class="flex items-center gap-3 w-full md:w-auto">
                                    <div class="w-8 h-8 rounded-lg bg-indigo-500/10 flex items-center justify-center text-indigo-400 shrink-0">
                                        <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z" />
                                        </svg>
                                    </div>
                                    <div class="flex-1">
                                        <div class="flex items-center gap-2 group">
                                            <span id="sensor-${mac}-title" class="text-sm font-bold text-slate-200">${sensor.display_name}</span>
                                            <button onclick="startEditSensorName('${mac}')" class="opacity-0 group-hover:opacity-100 transition-opacity p-0.5 hover:text-indigo-400" title="Edit Name">
                                                <svg class="w-3.5 h-3.5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15.232 5.232l3.536 3.536m-2.036-5.036a2.5 2.5 0 113.536 3.536L6.5 21.036H3v-3.572L16.732 3.732z" />
                                                </svg>
                                            </button>
                                        </div>
                                        <div id="sensor-${mac}-edit-container" class="hidden flex items-center gap-2 mt-1">
                                            <input id="sensor-${mac}-edit-input" type="text" class="bg-slate-900 border border-white/10 rounded-xl px-2 py-0.5 text-xs text-slate-100 focus:outline-none focus:border-indigo-500 w-48" />
                                            <button onclick="saveSensorName('${mac}')" class="bg-indigo-600 hover:bg-indigo-700 text-white rounded-lg px-2 py-0.5 text-[10px] font-bold transition-all">Save</button>
                                            <button onclick="cancelEditSensorName('${mac}')" class="text-slate-400 hover:text-slate-200 text-[10px] px-1">Cancel</button>
                                        </div>
                                        <p class="text-[10px] text-slate-400 mt-0.5">MAC: ${mac}</p>
                                    </div>
                                </div>

                                <!-- Middle: Temp, Humi, Battery -->
                                <div class="flex items-center gap-6 justify-center w-full md:w-auto flex-wrap">
                                    <!-- Temp -->
                                    <div class="flex items-baseline gap-1.5">
                                        <span class="text-xs text-slate-400 font-medium">Temp:</span>
                                        <span id="sensor-${mac}-temp" class="text-xl font-black tracking-tight">--°C</span>
                                    </div>
                                    <span class="w-px h-4 bg-white/10 hidden sm:block"></span>
                                    <!-- Humi -->
                                    <div class="flex items-baseline gap-1.5">
                                        <span class="text-xs text-slate-400 font-medium">Humidity:</span>
                                        <span id="sensor-${mac}-humi" class="text-xl font-black tracking-tight text-sky-400">--%</span>
                                    </div>
                                    <span class="w-px h-4 bg-white/10 hidden sm:block"></span>
                                    <!-- Battery -->
                                    <div class="flex items-center gap-2">
                                        <span class="text-xs text-slate-400 font-medium">Battery:</span>
                                        <div class="flex items-center gap-1.5">
                                            <svg id="sensor-${mac}-bat-icon" class="w-5 h-5" viewBox="0 0 24 24" fill="none" stroke="currentColor"></svg>
                                            <span id="sensor-${mac}-bat" class="text-sm font-bold text-slate-200">--%</span>
                                        </div>
                                    </div>
                                </div>

                                <!-- Right: Status and Time -->
                                <div class="flex items-center gap-3 w-full md:w-auto justify-between md:justify-end">
                                    <span id="sensor-${mac}-updated" class="text-[10px] text-slate-400">Updated: --</span>
                                    <div id="sensor-${mac}-status-badge" class="px-2.5 py-0.5 rounded-full text-[9px] font-bold tracking-wide uppercase">
                                        Loading
                                    </div>
                                </div>
                            `;
                            rowsContainer.appendChild(row);
                        }
                        
                        if (activeSensorEditMac !== mac) {
                            document.getElementById(`sensor-${mac}-title`).innerText = sensor.display_name;
                        }
                        
                        const tempEl = document.getElementById(`sensor-${mac}-temp`);
                        tempEl.innerText = `${sensor.temperature}°C`;
                        document.getElementById(`sensor-${mac}-humi`).innerText = `${sensor.humidity}%`;
                        document.getElementById(`sensor-${mac}-bat`).innerText = `${sensor.battery}%`;
                        
                        const batIcon = document.getElementById(`sensor-${mac}-bat-icon`);
                        batIcon.className = `w-5 h-5 ${getBatteryColorClass(sensor.battery)}`;
                        batIcon.innerHTML = getBatterySVG(sensor.battery);
                        
                        document.getElementById(`sensor-${mac}-updated`).innerText = `Updated: ${formatRelativeTime(sensor.timestamp)}`;
                        
                        const badge = document.getElementById(`sensor-${mac}-status-badge`);
                        if (sensor.stale) {
                            badge.innerText = 'STALE';
                            badge.className = 'px-2.5 py-0.5 rounded-full text-[9px] font-bold tracking-wide uppercase bg-rose-500/10 text-rose-400 border border-rose-500/20';
                            tempEl.className = 'text-xl font-black tracking-tight text-slate-500';
                        } else {
                            badge.innerText = 'ACTIVE';
                            badge.className = 'px-2.5 py-0.5 rounded-full text-[9px] font-bold tracking-wide uppercase bg-emerald-500/10 text-emerald-400 border border-emerald-500/20';
                            tempEl.className = 'text-xl font-black tracking-tight text-transparent bg-clip-text bg-gradient-to-r from-indigo-400 to-purple-400';
                        }
                    });
                    
                    const activeMacs = sensors.map(s => s.mac);
                    const existingRows = rowsContainer.querySelectorAll('[id^="sensor-row-"]');
                    existingRows.forEach(rowEl => {
                        const rowMac = rowEl.id.replace('sensor-row-', '');
                        if (!activeMacs.includes(rowMac)) {
                            rowEl.remove();
                        }
                    });
                }
            } catch (err) {
                console.error("Error fetching status:", err);
            }
        }

        let currentRange = '24h';

        function selectTimeRange(range) {
            currentRange = range;
            ['1h', '6h', '12h', '24h'].forEach(r => {
                const btn = document.getElementById(`btn-range-${r}`);
                if (!btn) return;
                if (r === range) {
                    btn.className = 'px-3 py-2 text-xs font-bold rounded-lg transition-all bg-indigo-500 text-white shadow shadow-indigo-500/20';
                } else {
                    btn.className = 'px-3 py-2 text-xs font-bold rounded-lg transition-all text-slate-400 hover:text-white';
                }
            });
            fetchHistory();
        }

        function selectChartUPS(upsId) {
            currentChartUPS = upsId;
            const btn1 = document.getElementById('btn-chart-ups1');
            const btn2 = document.getElementById('btn-chart-ups2');

            if (upsId === 'ups1') {
                btn1.className = 'px-4 py-2 text-xs font-bold rounded-lg transition-all bg-indigo-500 text-white shadow shadow-indigo-500/20';
                btn2.className = 'px-4 py-2 text-xs font-bold rounded-lg transition-all text-slate-400 hover:text-white';
            } else {
                btn2.className = 'px-4 py-2 text-xs font-bold rounded-lg transition-all bg-indigo-500 text-white shadow shadow-indigo-500/20';
                btn1.className = 'px-4 py-2 text-xs font-bold rounded-lg transition-all text-slate-400 hover:text-white';
            }

            renderCharts();
        }

        async function fetchHistory() {
            try {
                const now = new Date();
                let msOffset = 24 * 60 * 60 * 1000;
                if (currentRange === '1h') msOffset = 1 * 60 * 60 * 1000;
                else if (currentRange === '6h') msOffset = 6 * 60 * 60 * 1000;
                else if (currentRange === '12h') msOffset = 12 * 60 * 60 * 1000;
                
                const start = new Date(now.getTime() - msOffset);
                const pad = num => String(num).padStart(2, '0');
                const formatDate = date => `${date.getFullYear()}-${pad(date.getMonth() + 1)}-${pad(date.getDate())} ${pad(date.getHours())}:${pad(date.getMinutes())}:${pad(date.getSeconds())}`;
                
                const startStr = formatDate(start);
                const endStr = formatDate(now);
                
                const res = await fetch(`/api/history?start=${encodeURIComponent(startStr)}&end=${encodeURIComponent(endStr)}`);
                rawHistoryData = await res.json();
                renderCharts();
            } catch (err) {
                console.error("Error fetching history:", err);
            }
        }

        function renderCharts() {
            let dataList = rawHistoryData[currentChartUPS] || [];
            
            // Slice based on selected time range
            let pointsToKeep = 2880; // 24h at 30s interval
            if (currentRange === '1h') pointsToKeep = 120;
            else if (currentRange === '6h') pointsToKeep = 720;
            else if (currentRange === '12h') pointsToKeep = 1440;
            
            if (dataList.length > pointsToKeep) {
                dataList = dataList.slice(-pointsToKeep);
            }
            
            const labels = dataList.map(r => {
                if (!r.timestamp) return '';
                const parts = r.timestamp.split(' ');
                if (parts.length < 2) return r.timestamp;
                const timePart = parts[1];
                const timeSub = timePart.substring(0, 5); // "HH:MM"
                
                // Show date for longer ranges to avoid ambiguity across midnight
                if (currentRange === '12h' || currentRange === '24h') {
                    const datePart = parts[0];
                    const dateSub = datePart.substring(5); // "MM-DD"
                    return `${dateSub} ${timeSub}`;
                }
                return timeSub;
            });
            
            const charges = dataList.map(r => r.battery_charge_pct !== 'NA' ? parseFloat(r.battery_charge_pct) : null);
            const batVolts = dataList.map(r => r.battery_voltage !== 'NA' ? parseFloat(r.battery_voltage) : null);
            const inputVolts = dataList.map(r => r.input_voltage !== 'NA' ? parseFloat(r.input_voltage) : null);

            // Charge Chart
            if (chargeChart) chargeChart.destroy();
            const ctxCharge = document.getElementById('chart-charge').getContext('2d');
            chargeChart = new Chart(ctxCharge, {
                type: 'line',
                data: {
                    labels: labels,
                    datasets: [{
                        label: `${customNames[currentChartUPS]} Charge (%)`,
                        data: charges,
                        borderColor: 'rgb(99, 102, 241)',
                        backgroundColor: 'rgba(99, 102, 241, 0.1)',
                        borderWidth: 2,
                        pointRadius: 0,
                        fill: true,
                        tension: 0.2
                    }]
                },
                options: {
                    responsive: true,
                    maintainAspectRatio: false,
                    scales: {
                        x: { grid: { display: false }, ticks: { color: '#94a3b8', font: { size: 9 } } },
                        y: { min: 0, max: 100, ticks: { color: '#94a3b8', font: { size: 9 } }, grid: { color: 'rgba(255,255,255,0.05)' } }
                    },
                    plugins: { legend: { display: false } }
                }
            });

            // Voltage Chart
            if (voltageChart) voltageChart.destroy();
            const ctxVoltage = document.getElementById('chart-voltage').getContext('2d');
            voltageChart = new Chart(ctxVoltage, {
                type: 'line',
                data: {
                    labels: labels,
                    datasets: [
                        {
                            label: `${customNames[currentChartUPS]} Battery Voltage`,
                            data: batVolts,
                            borderColor: 'rgb(168, 85, 247)',
                            borderWidth: 2,
                            pointRadius: 0,
                            tension: 0.2,
                            yAxisID: 'y'
                        },
                        {
                            label: 'Input Voltage',
                            data: inputVolts,
                            borderColor: 'rgb(234, 179, 8)',
                            borderWidth: 1.5,
                            pointRadius: 0,
                            tension: 0.2,
                            yAxisID: 'y1'
                        }
                    ]
                },
                options: {
                    responsive: true,
                    maintainAspectRatio: false,
                    scales: {
                        x: { grid: { display: false }, ticks: { color: '#94a3b8', font: { size: 9 } } },
                        y: { 
                            type: 'linear',
                            display: true,
                            position: 'left',
                            title: { display: true, text: 'Battery (V)', color: '#a855f7', font: { size: 10 } },
                            ticks: { color: '#94a3b8', font: { size: 9 } },
                            grid: { color: 'rgba(255,255,255,0.05)' }
                        },
                        y1: {
                            type: 'linear',
                            display: true,
                            position: 'right',
                            title: { display: true, text: 'Input (V)', color: '#eab308', font: { size: 10 } },
                            ticks: { color: '#94a3b8', font: { size: 9 } },
                            grid: { drawOnChartArea: false }
                        }
                    },
                    plugins: { legend: { display: true, labels: { color: '#cbd5e1', font: { size: 10 } } } }
                }
            });
        }

        async function fetchBatteryHealth() {
            try {
                const res = await fetch('/api/battery-health');
                const data = await res.json();
                
                ['ups1', 'ups2'].forEach(id => {
                    const events = data[id] || [];
                    const tbody = document.getElementById(`health-table-${id}`);
                    const title = document.getElementById(`health-${id}-title`);
                    
                    if (title) {
                        title.innerText = `${customNames[id]} Health Events`;
                    }
                    
                    // Update upfront card health status
                    const healthDot = document.getElementById(`${id}-health-dot`);
                    const healthText = document.getElementById(`${id}-health-text`);
                    if (healthDot && healthText) {
                        if (events.length > 0) {
                            // Find the first event with a valid health score (not N/A)
                            const assessableEvent = events.find(e => e.health_score !== 'N/A');
                            if (assessableEvent) {
                                const score = assessableEvent.health_score;
                                const rating = assessableEvent.health_rating;
                                healthText.innerText = `Battery Health: ${score}% (${rating})`;
                                
                                healthDot.className = 'w-2.5 h-2.5 rounded-full';
                                if (rating === 'Excellent' || rating === 'Good') {
                                    healthDot.classList.add('bg-emerald-500');
                                } else if (rating === 'Fair') {
                                    healthDot.classList.add('bg-amber-500');
                                } else {
                                    healthDot.classList.add('bg-rose-500');
                                }
                            } else {
                                healthText.innerText = 'Battery Health: Unknown (Outages too short)';
                                healthDot.className = 'w-2.5 h-2.5 rounded-full bg-slate-500';
                            }
                        } else {
                            healthText.innerText = 'Battery Health: Unknown (No events logged)';
                            healthDot.className = 'w-2.5 h-2.5 rounded-full bg-slate-500';
                        }
                    }
                    
                    if (!tbody) return;
                    
                    if (events.length === 0) {
                        tbody.innerHTML = `
                            <tr>
                                <td colspan="5" class="py-4 text-center text-slate-500">No discharge events recorded yet.</td>
                            </tr>
                        `;
                        return;
                    }
                    
                    tbody.innerHTML = events.map(ev => {
                        let badgeColor = 'bg-emerald-500/10 text-emerald-400 border-emerald-500/20';
                        if (ev.health_rating === 'Replace Battery') {
                            badgeColor = 'bg-rose-500/10 text-rose-400 border-rose-500/20';
                        } else if (ev.health_rating === 'Fair') {
                            badgeColor = 'bg-amber-500/10 text-amber-400 border-amber-500/20';
                        } else if (ev.health_rating === 'Too Short to Assess') {
                            badgeColor = 'bg-slate-500/10 text-slate-400 border-slate-500/20';
                        }
                        
                        const scoreDisplay = ev.health_score === 'N/A' ? '' : `${ev.health_score}% `;
                        return `
                            <tr class="border-b border-white/5 hover:bg-white/5 transition-colors">
                                <td class="py-3 font-medium">${ev.date}</td>
                                <td class="py-3">${ev.duration_mins} mins</td>
                                <td class="py-3">${ev.start_voltage}V &rarr; ${ev.end_voltage}V</td>
                                <td class="py-3">${ev.drop_rate_v_hr} V/hr</td>
                                <td class="py-3 text-right">
                                    <span class="px-2 py-0.5 rounded-full text-[10px] font-bold border ${badgeColor}">
                                        ${scoreDisplay}(${ev.health_rating})
                                    </span>
                                </td>
                            </tr>
                        `;
                    }).join('');
                });
            } catch (err) {
                console.error("Error fetching battery health:", err);
            }
        }

        function toggleControlZone(id) {
            const zone = document.getElementById(`${id}-control-zone`);
            const arrow = document.getElementById(`${id}-control-arrow`);
            if (zone.classList.contains('hidden')) {
                zone.classList.remove('hidden');
                arrow.classList.add('rotate-180');
            } else {
                zone.classList.add('hidden');
                arrow.classList.remove('rotate-180');
            }
        }

        let activeModalUps = null;
        let activeModalAction = null;
        let expectedPhrase = "";

        function openConfirmModal(upsId, action) {
            activeModalUps = upsId;
            activeModalAction = action;
            
            const modal = document.getElementById('confirm-modal');
            const nameEl = document.getElementById('modal-ups-name');
            const expectedEl = document.getElementById('modal-expected-phrase');
            const inputEl = document.getElementById('modal-confirm-input');
            const confirmBtn = document.getElementById('modal-btn-confirm');
            const titleEl = document.getElementById('modal-title-text');
            const descEl = document.getElementById('modal-desc-text');
            const warningEl = document.getElementById('modal-warning-box');

            if (!modal || !nameEl || !expectedEl || !inputEl || !confirmBtn) return;

            const displayName = customNames[upsId] || (upsId === 'ups1' ? 'UPS Unit 1' : 'UPS Unit 2');
            nameEl.innerText = displayName;
            inputEl.value = "";
            
            if (action === 'off') {
                expectedPhrase = 'TURN OFF';
                titleEl.innerText = "Confirm Load Power Cut";
                descEl.innerHTML = `You are about to turn <span class="font-bold text-rose-400">OFF</span> the load outlets for <span class="font-bold text-slate-100">${displayName}</span>. This will immediately cut power to all connected equipment!`;
                warningEl.classList.remove('hidden');
                confirmBtn.innerText = "Turn Off Load";
                confirmBtn.className = "flex-1 bg-rose-600 hover:bg-rose-700 text-white rounded-xl py-2 text-sm font-semibold transition-all opacity-50 cursor-not-allowed shadow-lg shadow-rose-600/20";
            } else if (action === 'on') {
                expectedPhrase = 'TURN ON';
                titleEl.innerText = "Confirm Load Power Restore";
                descEl.innerHTML = `You are about to turn <span class="font-bold text-emerald-400">ON</span> the load outlets for <span class="font-bold text-slate-100">${displayName}</span>. This will restore power to connected equipment.`;
                warningEl.classList.add('hidden');
                confirmBtn.innerText = "Turn On Load";
                confirmBtn.className = "flex-1 bg-emerald-600 hover:bg-emerald-700 text-white rounded-xl py-2 text-sm font-semibold transition-all opacity-50 cursor-not-allowed shadow-lg shadow-emerald-600/20";
            } else if (action === 'shutdown_return') {
                expectedPhrase = 'SHUTDOWN RETURN';
                titleEl.innerText = "Confirm Shutdown & Return";
                descEl.innerHTML = `You are about to initiate a delayed shutdown sequence for <span class="font-bold text-slate-100">${displayName}</span>. Power to outlets will turn off, and automatically restore once grid power returns.`;
                warningEl.classList.remove('hidden');
                confirmBtn.innerText = "Shutdown & Return";
                confirmBtn.className = "flex-1 bg-amber-600 hover:bg-amber-700 text-white rounded-xl py-2 text-sm font-semibold transition-all opacity-50 cursor-not-allowed shadow-lg shadow-amber-600/20";
            } else if (action === 'shutdown_stayoff') {
                expectedPhrase = 'SHUTDOWN STAYOFF';
                titleEl.innerText = "Confirm Shutdown & Stay Off";
                descEl.innerHTML = `You are about to initiate a delayed shutdown sequence for <span class="font-bold text-slate-100">${displayName}</span>. Power to outlets will turn off and remain off until manually powered back on.`;
                warningEl.classList.remove('hidden');
                confirmBtn.innerText = "Shutdown & Stay Off";
                confirmBtn.className = "flex-1 bg-rose-600 hover:bg-rose-700 text-white rounded-xl py-2 text-sm font-semibold transition-all opacity-50 cursor-not-allowed shadow-lg shadow-rose-600/20";
            } else if (action === 'shutdown_stop') {
                expectedPhrase = 'CANCEL SHUTDOWN';
                titleEl.innerText = "Cancel Shutdown Sequence";
                descEl.innerHTML = `You are about to cancel any pending shutdown timers or sequences in progress for <span class="font-bold text-slate-100">${displayName}</span>.`;
                warningEl.classList.add('hidden');
                confirmBtn.innerText = "Cancel Shutdown";
                confirmBtn.className = "flex-1 bg-indigo-600 hover:bg-indigo-700 text-white rounded-xl py-2 text-sm font-semibold transition-all opacity-50 cursor-not-allowed shadow-lg shadow-indigo-600/20";
            }

            expectedEl.innerText = expectedPhrase;
            confirmBtn.disabled = true;
            modal.classList.remove('hidden');
        }

        function closeConfirmModal() {
            const modal = document.getElementById('confirm-modal');
            if (modal) modal.classList.add('hidden');
            activeModalUps = null;
            activeModalAction = null;
            expectedPhrase = "";
        }

        function validateConfirmPhrase() {
            const inputVal = document.getElementById('modal-confirm-input').value.trim();
            const confirmBtn = document.getElementById('modal-btn-confirm');
            if (!confirmBtn) return;

            if (inputVal.toUpperCase() === expectedPhrase) {
                confirmBtn.disabled = false;
                confirmBtn.classList.remove('opacity-50', 'cursor-not-allowed');
            } else {
                confirmBtn.disabled = true;
                confirmBtn.classList.add('opacity-50', 'cursor-not-allowed');
            }
        }

        async function executeLoadAction() {
            if (!activeModalUps || !activeModalAction) return;
            
            const confirmBtn = document.getElementById('modal-btn-confirm');
            const cancelBtn = document.getElementById('modal-btn-cancel');
            const inputEl = document.getElementById('modal-confirm-input');
            
            if (confirmBtn) confirmBtn.disabled = true;
            if (cancelBtn) cancelBtn.disabled = true;
            if (inputEl) inputEl.disabled = true;

            try {
                const res = await fetch('/api/load/control', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({
                        ups: activeModalUps,
                        action: activeModalAction
                    })
                });

                if (res.ok) {
                    closeConfirmModal();
                    await fetchStatus();
                } else {
                    const data = await res.json();
                    alert(`Action failed: ${data.error || 'Unknown error'}`);
                }
            } catch (err) {
                console.error("Error running load control:", err);
                alert("Network error running load control");
            } finally {
                if (confirmBtn) confirmBtn.disabled = false;
                if (cancelBtn) cancelBtn.disabled = false;
                if (inputEl) {
                    inputEl.disabled = false;
                    inputEl.value = "";
                }
                closeConfirmModal();
            }
        }

        async function toggleBeeper(id) {
            const btn = document.getElementById(`${id}-beeper-btn`);
            if (!btn || btn.disabled) return;
            
            // Disable button temporarily to prevent double click
            btn.disabled = true;
            btn.classList.add('opacity-50', 'cursor-not-allowed');
            
            try {
                const res = await fetch('/api/beeper/toggle', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ ups: id })
                });
                
                if (res.ok) {
                    await fetchStatus();
                } else {
                    const data = await res.json();
                    alert(`Failed to toggle beeper: ${data.error || 'Unknown error'}`);
                }
            } catch (err) {
                console.error("Error toggling beeper:", err);
                alert("Network error toggling beeper");
            } finally {
                btn.disabled = false;
                btn.classList.remove('opacity-50', 'cursor-not-allowed');
            }
        }

        async function saveShutdownDelay(id) {
            const input = document.getElementById(`${id}-delay-shutdown-input`);
            const btn = document.getElementById(`${id}-delay-shutdown-btn`);
            if (!input || !btn || btn.disabled) return;
            
            const val = parseInt(input.value);
            if (isNaN(val) || val < 12 || val > 540) {
                alert("Shutdown delay must be a number between 12 and 540 seconds.");
                return;
            }
            
            btn.disabled = true;
            btn.classList.add('opacity-50', 'cursor-not-allowed');
            input.disabled = true;
            
            try {
                const res = await fetch('/api/config/variable', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({
                        ups: id,
                        var: 'ups.delay.shutdown',
                        value: val.toString()
                    })
                });
                
                if (res.ok) {
                    // Flash input green on success
                    input.classList.remove('border-white/10');
                    input.classList.add('border-emerald-500', 'bg-emerald-500/10');
                    setTimeout(() => {
                        input.classList.remove('border-emerald-500', 'bg-emerald-500/10');
                        input.classList.add('border-white/10');
                    }, 1500);
                    await fetchStatus();
                } else {
                    const data = await res.json();
                    alert(`Failed to set shutdown delay: ${data.error || 'Unknown error'}`);
                }
            } catch (err) {
                console.error("Error setting shutdown delay:", err);
                alert("Network error setting shutdown delay");
            } finally {
                btn.disabled = false;
                btn.classList.remove('opacity-50', 'cursor-not-allowed');
                input.disabled = false;
            }
        }

        async function saveStartupDelay(id) {
            const input = document.getElementById(`${id}-delay-start-input`);
            const btn = document.getElementById(`${id}-delay-start-btn`);
            if (!input || !btn || btn.disabled) return;
            
            const val = parseInt(input.value);
            if (isNaN(val) || val < 60 || val > 599940) {
                alert("Startup delay must be a number between 60 and 599,940 seconds.");
                return;
            }
            
            btn.disabled = true;
            btn.classList.add('opacity-50', 'cursor-not-allowed');
            input.disabled = true;
            
            try {
                const res = await fetch('/api/config/variable', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({
                        ups: id,
                        var: 'ups.delay.start',
                        value: val.toString()
                    })
                });
                
                if (res.ok) {
                    // Flash input green on success
                    input.classList.remove('border-white/10');
                    input.classList.add('border-emerald-500', 'bg-emerald-500/10');
                    setTimeout(() => {
                        input.classList.remove('border-emerald-500', 'bg-emerald-500/10');
                        input.classList.add('border-white/10');
                    }, 1500);
                    await fetchStatus();
                } else {
                    const data = await res.json();
                    alert(`Failed to set startup delay: ${data.error || 'Unknown error'}`);
                }
            } catch (err) {
                console.error("Error setting startup delay:", err);
                alert("Network error setting startup delay");
            } finally {
                btn.disabled = false;
                btn.classList.remove('opacity-50', 'cursor-not-allowed');
                input.disabled = false;
            }
        }

        function scrollToFirmwareSettings() {
            const el = document.getElementById('section-firmware');
            if (el) el.scrollIntoView({ behavior: 'smooth' });
        }

        async function checkFirmwareOnLoad() {
            try {
                const res = await fetch('/api/firmware/check');
                if (res.ok) {
                    const data = await res.json();
                    
                    const curDisplays = ['current-version-display', 'system-version-card-text'];
                    curDisplays.forEach(id => {
                        const el = document.getElementById(id);
                        if (el) el.innerText = data.current_version;
                    });

                    if (data.update_available) {
                        const badge = document.getElementById('firmware-update-badge');
                        if (badge) {
                            badge.classList.remove('hidden');
                            badge.querySelector('span:last-child').innerText = `🎁 Update Available (${data.latest_version})`;
                        }
                        const appBadge = document.getElementById('update-available-badge');
                        if (appBadge) appBadge.classList.remove('hidden');
                    }
                }
            } catch (err) {
                console.error("Error auto-checking updates:", err);
            }
        }

        async function checkForUpdates() {
            const btn = document.getElementById('btn-check-updates');
            const statusContainer = document.getElementById('update-status-container');
            const statusText = document.getElementById('update-status-text');
            const selectorContainer = document.getElementById('version-selector-container');
            const select = document.getElementById('version-select');
            const appBadge = document.getElementById('update-available-badge');
            
            btn.disabled = true;
            btn.classList.add('opacity-50', 'cursor-not-allowed');
            statusContainer.classList.remove('hidden');
            statusText.innerText = "Checking for updates...";
            appBadge.classList.add('hidden');
            selectorContainer.classList.add('hidden');
            
            try {
                const res = await fetch('/api/firmware/check');
                if (res.ok) {
                    const data = await res.json();
                    
                    if (data.versions && data.versions.length > 0) {
                        statusText.innerText = data.update_available 
                            ? `New update found: ${data.latest_version} (Current: ${data.current_version})`
                            : `Your software is up to date (Current: ${data.current_version})`;
                            
                        if (data.update_available) {
                            appBadge.classList.remove('hidden');
                        }
                        
                        select.innerHTML = data.versions.map(v => 
                            `<option value="${v}">${v}${v === data.current_version ? ' (Current)' : ''}</option>`
                        ).join('');
                        
                        selectorContainer.classList.remove('hidden');
                    } else {
                        statusText.innerText = "No versions found on repository releases.";
                    }
                } else {
                    statusText.innerText = "Failed to fetch version repository.";
                }
            } catch (err) {
                console.error("Error manual checking updates:", err);
                statusText.innerText = "Error contacting update server.";
            } finally {
                btn.disabled = false;
                btn.classList.remove('opacity-50', 'cursor-not-allowed');
            }
        }

        let updatePollingInterval = null;

        async function installSelectedVersion() {
            const select = document.getElementById('version-select');
            const targetVersion = select.value;
            if (!targetVersion) return;
            
            if (!confirm(`Are you sure you want to install version ${targetVersion}?`)) {
                return;
            }
            
            const progressCard = document.getElementById('update-progress-card');
            const progressBar = document.getElementById('update-progress-bar');
            const log = document.getElementById('update-log');
            const checkBtn = document.getElementById('btn-check-updates');
            const installBtn = document.getElementById('btn-install-version');
            
            checkBtn.disabled = true;
            installBtn.disabled = true;
            progressCard.classList.remove('hidden');
            progressBar.style.width = '10%';
            log.innerHTML = `<div>[info] Initiating installation of ${targetVersion}...</div>`;
            
            try {
                log.innerHTML += `<div>[info] Downloading code from GitHub...</div>`;
                progressBar.style.width = '30%';
                
                const res = await fetch('/api/firmware/update', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ version: targetVersion })
                });
                
                const data = await res.json();
                if (res.ok && data.status === 'success') {
                    progressBar.style.width = '70%';
                    log.innerHTML += `<div>[success] ${data.message}</div>`;
                    log.innerHTML += `<div>[info] Reconnecting to system dashboard...</div>`;
                    progressBar.style.width = '90%';
                    
                    let pollCount = 0;
                    updatePollingInterval = setInterval(async () => {
                        pollCount++;
                        log.innerHTML += `<div>[info] Connection attempt ${pollCount}...</div>`;
                        log.scrollTop = log.scrollHeight;
                        
                        try {
                            const testRes = await fetch('/api/status');
                            if (testRes.ok) {
                                clearInterval(updatePollingInterval);
                                progressBar.style.width = '100%';
                                log.innerHTML += `<div>[success] Dashboard is online! Reloading page...</div>`;
                                log.scrollTop = log.scrollHeight;
                                setTimeout(() => {
                                    window.location.reload();
                                }, 1500);
                            }
                        } catch (e) {
                            // Expected offline during reboot
                        }
                        
                        if (pollCount > 30) {
                            clearInterval(updatePollingInterval);
                            log.innerHTML += `<div>[error] Connection timeout. Please check service status on the server.</div>`;
                            log.scrollTop = log.scrollHeight;
                            checkBtn.disabled = false;
                            installBtn.disabled = false;
                        }
                    }, 2000);
                    
                } else {
                    progressBar.style.width = '0%';
                    log.innerHTML += `<div class="text-rose-400">[error] ${data.error || 'Update failed'}</div>`;
                    checkBtn.disabled = false;
                    installBtn.disabled = false;
                }
            } catch (err) {
                console.error("Installation network error:", err);
                progressBar.style.width = '0%';
                log.innerHTML += `<div class="text-rose-400">[error] Connection lost during update command.</div>`;
                checkBtn.disabled = false;
                installBtn.disabled = false;
            }
            log.scrollTop = log.scrollHeight;
        }

        // Init
        fetchStatus();
        fetchHistory();
        fetchBatteryHealth();
        checkFirmwareOnLoad();
        
        // Refresh loops
        setInterval(fetchStatus, 5000);         // Live status every 5s
        setInterval(fetchHistory, 30000);       // Reload logs every 30s
        setInterval(fetchBatteryHealth, 30000); // Reload health logs every 30s
    </script>

    <!-- Confirmation Modal -->
    <div id="confirm-modal" class="hidden fixed inset-0 z-50 flex items-center justify-center p-4 bg-slate-950/80 backdrop-blur-sm">
        <div class="glass max-w-md w-full rounded-3xl p-6 space-y-6 border border-rose-500/20 shadow-2xl shadow-rose-950/20">
            <div class="flex items-center gap-3 text-rose-400" id="modal-title-container">
                <div class="w-10 h-10 rounded-xl bg-rose-500/10 flex items-center justify-center">
                    <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z" />
                    </svg>
                </div>
                <h3 id="modal-title-text" class="text-lg font-bold tracking-tight">Confirm Load Power Cut</h3>
            </div>
            
            <p id="modal-desc-text" class="text-sm text-slate-300 leading-relaxed">
                You are about to turn <span class="font-bold text-rose-400">OFF</span> the load outlets for <span id="modal-ups-name" class="font-bold text-slate-100"></span>. This will immediately cut power to all connected equipment!
            </p>
            
            <div id="modal-warning-box" class="bg-rose-500/5 border border-rose-500/10 rounded-2xl p-3 text-xs text-rose-300 space-y-1">
                <span class="font-semibold block text-rose-400">WARNING:</span>
                If this Orange Pi server is powered by this UPS unit, it will shut down instantly and the web dashboard will lose connection.
            </div>

            <div class="space-y-2">
                <label for="modal-confirm-input" class="text-xs text-slate-400 font-medium">To confirm, type <span id="modal-expected-phrase" class="font-mono bg-slate-900 border border-white/5 px-1.5 py-0.5 rounded text-rose-400"></span> below:</label>
                <input id="modal-confirm-input" oninput="validateConfirmPhrase()" type="text" class="w-full bg-slate-900 border border-white/10 rounded-xl px-3 py-2 text-sm text-slate-100 focus:outline-none focus:border-rose-500" placeholder="Type confirmation here..." />
            </div>

            <div class="flex gap-3">
                <button id="modal-btn-cancel" onclick="closeConfirmModal()" class="flex-1 bg-white/5 hover:bg-white/10 text-slate-300 border border-white/10 rounded-xl py-2 text-sm font-semibold transition-all">Cancel</button>
                <button id="modal-btn-confirm" onclick="executeLoadAction()" disabled class="flex-1 bg-rose-600 hover:bg-rose-700 text-white rounded-xl py-2 text-sm font-semibold transition-all opacity-50 cursor-not-allowed shadow-lg shadow-rose-600/20">Turn Off Load</button>
            </div>
        </div>
    </div>
</body>
</html>
"""
