import { 
  Maximize2, Activity, Map, Wind, AlertTriangle, 
  Video, Mic2, BatteryCharging 
} from 'lucide-react';
import F1Leaderboard from './leaderboard';
import { useEffect, useState, useRef, useCallback, memo } from 'react';
import FastestLapBadge from './fastestlap';
import CircuitMap from './circuitmap';

// 1. Componente "Bento Card" Reutilizable (El bloque constructor)
const BentoCard = ({ children, className = "", title, icon: Icon }) => (
  <div className={`bg-[#15151e] border border-gray-800 rounded-2xl overflow-hidden flex flex-col hover:border-gray-600 transition-all duration-300 shadow-xl ${className}`}>
    {/* Header opcional de la tarjeta */}
    {title && (
      <div className="px-4 py-3 border-b border-gray-800/50 flex justify-between items-center bg-[#1a1a24]">
        <h3 className="text-xs font-bold uppercase tracking-widest text-gray-400 flex items-center gap-2">
          {Icon && <Icon size={14} className="text-red-500" />}
          {title}
        </h3>
        <button className="text-gray-600 hover:text-white transition-colors">
          <Maximize2 size={12} />
        </button>
      </div>
    )}
    {/* Contenido */}
    <div className="flex-1 overflow-hidden relative">
      {children}
    </div>
  </div>
);

// 2. Componentes Mock (Rellenos para el grid)
const TelemetryGraph = () => (
  <div className="w-full h-full p-4 flex flex-col justify-end">
    <div className="flex justify-between text-[10px] text-gray-500 mb-2 font-mono">
      <span>THROTTLE</span>
      <span className="text-green-500">100%</span>
    </div>
    {/* Gráfico SVG Fake */}
    <div className="h-16 w-full flex items-end gap-1">
      {[40, 60, 45, 80, 100, 100, 100, 85, 60, 90, 100, 100, 95].map((h, i) => (
        <div key={i} className="flex-1 bg-green-500/20 rounded-t-sm relative group">
           <div style={{ height: `${h}%` }} className="absolute bottom-0 w-full bg-green-500 rounded-t-sm transition-all duration-500"></div>
        </div>
      ))}
    </div>
    <div className="flex justify-between text-[10px] text-gray-500 mt-2 font-mono border-t border-gray-800 pt-2">
      <span>BRAKE</span>
      <span className="text-red-500">0%</span>
    </div>
  </div>
);

const TrackMap = () => (
  <div className="w-full h-full flex items-center justify-center relative bg-[#121218]">
    {/* SVG Mapa Circuito (Simplificado) */}
    <svg viewBox="0 0 200 150" className="w-3/4 h-3/4 stroke-white fill-none stroke-2 opacity-80 drop-shadow-[0_0_10px_rgba(255,255,255,0.3)]">
      <path d="M40,120 L160,120 Q180,120 180,100 L180,50 Q180,30 160,30 L100,30 Q80,30 80,50 L80,80 Q80,100 60,100 L40,100 Q20,100 20,80 L20,60 Q20,40 40,40 Z" />
      {/* Puntos de pilotos */}
      <circle cx="160" cy="120" r="4" fill="#3671C6" className="animate-pulse" /> {/* Max */}
      <circle cx="140" cy="120" r="4" fill="#FF8000" /> {/* Lando */}
    </svg>
    <div className="absolute top-4 left-4 text-[10px] font-mono text-gray-500">
      SECTOR 2 <br/> <span className="text-yellow-400">YELLOW FLAG</span>
    </div>
  </div>
);

const RaceControl = () => (
  <div className="p-4 space-y-3 font-mono text-xs">
    <div className="flex gap-3 text-gray-300">
      <span className="text-gray-500">14:02</span>
      <span>TURN 4 INCIDENT NOTED</span>
    </div>
    <div className="flex gap-3 text-yellow-400">
      <span className="text-gray-500">14:05</span>
      <AlertTriangle size={12} className="inline mr-1"/>
      YELLOW FLAG SECTOR 2
    </div>
    <div className="flex gap-3 text-gray-300">
      <span className="text-gray-500">14:08</span>
      <span>DRS ENABLED</span>
    </div>
  </div>
);

const PauseButton = memo(({ onPause, onResume, handlex2, handlex3 }) => (
  <div>
    <button className="w-full h-full bg-gray-800 flex items-center justify-center text-gray-400 hover:text-white transition-colors" onClick={onPause}>Pause</button>
    <button className="w-full h-full bg-gray-800 flex items-center justify-center text-gray-400 hover:text-white transition-colors" onClick={onResume}>Resume</button>
    <button className="w-full h-full bg-gray-800 flex items-center justify-center text-gray-400 hover:text-white transition-colors" onClick={handlex2}>Velocidad x2</button>
    <button className="w-full h-full bg-gray-800 flex items-center justify-center text-gray-400 hover:text-white transition-colors" onClick={handlex3}>Velocidad x3</button>
  </div>
));

// 3. Layout Principal (El Grid)
const F1DashboardGrid = () => {

    const [cars, setCars] = useState([]);
    const [raceMeta, setRaceMeta] = useState(null);

    const socketRef = useRef(null);

    useEffect(() => {

        const ws = new WebSocket('ws://127.0.0.1:8000/race/ws');

        ws.onopen = () => {
            console.log("Conectado al Live Timing");
            socketRef.current = ws; // Guardamos la referencia del socket
        };

        ws.onmessage = (event) => {
            try {
                const data = JSON.parse(event.data);

                if (data?.payload) {
                  if (data.payload.cars) {
                    setCars(data.payload.cars);
                  }
                  if  (data.payload.race) {
                    setRaceMeta(data.payload.race);
                  }
                }

            } catch (error) {
                console.error("Error parseando datos:", error);
            }
        };

        ws.onerror = (error) => console.error("Error en WS:", error);

        return () => {
            ws.close();
            };
    }, []); 

    const handlePause = useCallback(() => {
      if (socketRef.current && socketRef.current.readyState === WebSocket.OPEN) {
        socketRef.current.send(JSON.stringify({ type: "pause" }));
        console.log("Comando PAUSE enviado");
      }
    }, []);

    const handleResume = useCallback(() => {
      if (socketRef.current && socketRef.current.readyState === WebSocket.OPEN) {
        socketRef.current.send(JSON.stringify({ type: "resume" }));
        console.log("Comando RESUME enviado");
      }
    }, []);

    const handlex2 = useCallback(() => {
      if (socketRef.current && socketRef.current.readyState === WebSocket.OPEN) {
        socketRef.current.send(JSON.stringify({ type: "set_time_scale", value: 2.0 }));
        console.log("Comando SET_TIME_SCALE 2.0 enviado");
      }
    }, []);

    const handlex3 = useCallback(() => {
      if (socketRef.current && socketRef.current.readyState === WebSocket.OPEN) {
        socketRef.current.send(JSON.stringify({ type: "set_time_scale", value: 3.0 }));
        console.log("Comando SET_TIME_SCALE 3.0 enviado");
      }
    }, []);

  return (
    <div className="min-h-screen bg-black text-white p-4 md:p-6 font-sans selection:bg-red-500 selection:text-white">
      
      {/* Navbar Simple */}
      <header className="flex justify-between items-center mb-6 px-2">
        <h1 className="text-2xl font-black tracking-tighter italic">
          F1<span className="text-red-600">TV</span> <span className="font-normal text-gray-500 text-lg not-italic tracking-normal ml-2">PRO DASHBOARD</span>
        </h1>
        <div className="flex gap-4">
            <button className="bg-red-600 hover:bg-red-700 px-4 py-1 rounded text-xs font-bold uppercase transition-colors">Live</button>
            <div className="w-8 h-8 rounded-full bg-gray-800 flex items-center justify-center text-xs">JP</div>
        </div>
      </header>

      {/* --- GRID LAYOUT --- 
          Definimos 4 columnas en desktop grande (lg), 3 en mediano (md) y 1 en movil.
          La altura de las filas se ajusta automáticamente o definimos alturas fijas.
      */}
      <div className="grid grid-cols-1 md:grid-cols-3 lg:grid-cols-4 grid-rows-[300px_250px_250px] gap-4">
        
        {/* 1. Main Feed (Video) - Ocupa 2 columnas y 1 fila */}
        <BentoCard className="col-span-1 md:col-span-2 lg:col-span-3 row-span-1 group relative" title="International Feed" icon={Video}>
           <div className="w-full h-full bg-gray-900 flex items-center justify-center relative">
              {/* Overlay simulado */}
              <div className="absolute top-4 right-4 bg-black/60 px-2 py-1 rounded text-[10px] font-mono flex items-center gap-2">
                 <div className="w-2 h-2 rounded-full bg-red-600 animate-pulse"></div> LIVE
              </div>
              <p className="text-gray-600 font-bold text-2xl group-hover:text-gray-500 transition-colors">NO SIGNAL</p>
           </div>
        </BentoCard>

        {/* 2. Leaderboard - Ocupa 1 columna pero se estira 2 filas (alto) */}
        <BentoCard className="col-span-1 md:col-span-1 lg:col-span-1 row-span-3 overflow-y-auto custom-scrollbar" title="Leaderboard">
          {/* Aquí inyectamos el componente F1Leaderboard que hicimos antes */}
          <div className="p-2">
             {raceMeta?.fastest_lap && 
             <FastestLapBadge driverName={raceMeta.fastest_lap_car} lapTime={raceMeta.fastest_lap} />
             }
             <F1Leaderboard drivers={cars || []}/> 
             {/* Nota: Asegúrate de quitar el 'w-full max-w-4xl' del componente Leaderboard anterior para que se ajuste al contenedor del grid */}
          </div>
        </BentoCard>

        {/* 3. Track Map - Ocupa 1 columna */}
        <BentoCard className="col-span-1 md:col-span-1 lg:col-span-1 row-span-1" title="Tracker" icon={Map}>
          {/* <TrackMap /> */}

          <CircuitMap drivers= {cars}/>
        
        </BentoCard>

        {/* 4. Onboard Camera - Ocupa 1 columna */}
        <BentoCard className="col-span-1 md:col-span-1 lg:col-span-1 row-span-1" title="Verstappen Onboard" icon={Video}>
           <div className="w-full h-full bg-gray-800 relative">
              <div className="absolute bottom-4 left-4 right-4">
                 <div className="flex justify-between items-end">
                    <div className="bg-black/50 px-2 py-1 rounded text-[10px] font-mono border border-white/20">
                       SPEED <span className="text-xl font-bold block text-white">302</span>
                    </div>
                    <div className="flex gap-1">
                        <div className="w-1 h-4 bg-green-500"></div>
                        <div className="w-1 h-6 bg-green-500"></div>
                        <div className="w-1 h-10 bg-green-500"></div>
                    </div>
                 </div>
              </div>
           </div>
        </BentoCard>

        {/* 5. Telemetry - Ocupa 1 columna */}
        <BentoCard className="col-span-1 md:col-span-1 lg:col-span-1 row-span-1" title="Telemetry" icon={Activity}>
          <TelemetryGraph />
        </BentoCard>

        <BentoCard className="col-span-1 md:col-span-1 lg:col-span-1 row-span-1 flex" title="Controls" icon={Activity}>
            <PauseButton onPause={handlePause} onResume={handleResume} handlex2={handlex2} handlex3={handlex3} />
        </BentoCard> 

        {/* 6. Race Control - Ocupa 1 columna (o 2 dependiendo del espacio) */}
        <BentoCard className="col-span-1 md:col-span-2 lg:col-span-2 row-span-1" title="Race Control" icon={Mic2}>
           <RaceControl />
        </BentoCard>

      </div>
    </div>
  );
};

export default F1DashboardGrid;