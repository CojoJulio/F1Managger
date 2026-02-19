import { Timer } from 'lucide-react';

const FastestLapBadge = ({ driverName, lapTime, teamColor = '#9B51E0' }) => {
  return (
    <div className="flex items-center bg-[#1f1f27] border border-purple-500/30 rounded-lg overflow-hidden shadow-[0_0_15px_rgba(155,81,224,0.15)] max-w-s mb-2">
      {/* Indicador Morado Lateral */}
      <div className="w-1.5 h-12 bg-purple-600 shadow-[0_0_10px_rgba(168,85,247,0.5)]"></div>
      
      <div className="flex flex-col px-3 py-1">
        <div className="flex items-center gap-2">
          <span className="text-[10px] font-black text-purple-400 uppercase tracking-tighter">
            Fastest Lap
          </span>
          <Timer size={12} className="text-purple-400 animate-pulse" />
        </div>
        
        <div className="flex items-baseline gap-4">
          <span className="text-sm font-bold text-white uppercase truncate max-w-[150px]">
            {driverName}
          </span>
          <span className="text-sm font-mono font-bold text-purple-500">
            {Math.floor(lapTime / 60)}:{(lapTime % 60).toFixed(3)}
          </span> 
        </div>
      </div>

      {/* Mini barra de equipo al final (opcional) */}
      <div 
        className="ml-auto h-6 w-1 rounded-full mr-2" 
        style={{ backgroundColor: teamColor }}
      ></div>
    </div>
  );
};

export default FastestLapBadge;