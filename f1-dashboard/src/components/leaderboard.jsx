import { Clock, TrendingUp, TrendingDown, Minus } from 'lucide-react';
import { useEffect, useState, memo} from 'react';


// 2. Componente para el icono del neumático (Soft, Medium, Hard)
const TyreBadge = ({ type, age }) => {
  const colors = {
    'S': 'border-red-500 text-red-500',   // Soft
    'M': 'border-yellow-400 text-yellow-400', // Medium
    'H': 'border-white text-white',       // Hard
    'I': 'border-green-500 text-green-500', // Inter
    'W': 'border-blue-500 text-blue-500'    // Wet
  };

  return (
    <div className="flex items-center gap-2">
      <div className={`w-6 h-6 rounded-full border-2 ${colors[type] || 'border-gray-500'} flex items-center justify-center text-xs font-bold bg-gray-900`}>
        {type}
      </div>
      <span className="text-gray-400 text-xs">{age}%</span>
    </div>
  );
};

// 3. Componente Principal
const F1Leaderboard = (data) => {
    const [drivers, setDrivers] = useState([]);

    useEffect(() => {
        setDrivers(data.drivers || []);
    }, [data]); 

   
  return (
    <div className="w-full max-w-4xl mx-auto bg-[#15151e] text-white font-sans rounded-xl overflow-hidden shadow-2xl border border-gray-800">
      
      {/* Header */}
      <div className="bg-[#1f1f27] p-4 border-b border-gray-700 flex justify-between items-center">
        <h2 className="text-xl font-bold tracking-wider uppercase flex items-center gap-2">
          <span className="w-2 h-6 bg-red-600 inline-block rounded-sm"></span>
          Live Timing
        </h2>


        <div className="flex gap-4 text-sm text-gray-400">
          <span className="flex items-center gap-1"><Clock size={16}/> LAP 24/53</span>
          <span className="text-red-500 font-bold animate-pulse">LIVE</span>
        </div>
      </div>

      {/* Tabla */}
      <div className="w-full">
        {/* Cabeceras de columna */}
        <div className="grid grid-cols-11 text-xs text-gray-400 uppercase tracking-widest px-4 py-2 border-b border-gray-800">
          <div className="col-span-1 text-center">Pos</div>
          <div className="col-span-4">Driver</div>
          <div className="col-span-1 text-right">Gap</div>
          <div className="col-span-3 text-right">Last Lap</div>
          <div className="col-span-2 text-center">Tyre</div>
        </div>

        {/* Filas de Pilotos */}
        <div className="divide-y divide-gray-800/50">
          {drivers.map((driver, index) => (
            <div 
              key={driver.pilot.id} 
              className="grid grid-cols-11 items-center px-4 py-3 hover:bg-[#2a2a35] transition-colors duration-200 group cursor-default"
            >
              {/* Posición */}
              <div className="col-span-1 text-center font-bold text-lg font-mono">
                {driver.state.position}
              </div>

              {/* Nombre y Equipo (Con barra de color) */}
              <div className="col-span-4 flex items-center gap-3">
                <div 
                  className="w-1 h-8 rounded-full shadow-[0_0_8px_rgba(0,0,0,0.5)]" 
                  style={{ backgroundColor: driver.team.team_color || '#555' }}
                />
                <div className="flex flex-col">
                  <span className="font-bold text-xs tracking-wide uppercase text-white group-hover:text-red-500 transition-colors">
                    {driver.pilot.name}
                  </span>
                  <span className="text-[10px] text-gray-500 uppercase font-semibold">
                    '{driver.team.name}'
                  </span>
                </div>
              </div>

              {/* Intervalo / Gap */}
              <div className="col-span-1 text-right font-mono text-sm text-yellow-400">
                {driver.state.gap_to_leader ? (
                  driver.state.gap_to_leader > 0 ? `+${driver.state.gap_to_leader.toFixed(3)}s` : `-${Math.abs(driver.state.gap_to_leader).toFixed(3)}s`
                ) : (
                  "Leader"
                )}
              </div>

              {/* Tiempo Última Vuelta */}
              <div className="col-span-3 text-right font-mono text-sm text-gray-300">
                {driver.lap_history && driver.lap_history.length > 0 ? (
                  `${(driver.lap_history[driver.lap_history.length - 1] / 60).toFixed(0)}:${(driver.lap_history[driver.lap_history.length - 1] % 60).toFixed(3)}`
                ) : (
                  "--:--"
                )}
              </div>

              {/* Neumáticos */}
              <div className="col-span-2 flex justify-center">
                <TyreBadge type={driver.tyre.compound.toUpperCase()[0]} age={driver.tyre.wear.toFixed(0)} />
              </div>

            </div>
          ))}
        </div>
      </div>
      
      {/* Footer / Status */}
      <div className="bg-[#1f1f27] p-2 text-center text-[10px] text-gray-500 border-t border-gray-800 uppercase tracking-widest">
        Official Data Stream • Weather: Dry 28°C
      </div>
    </div>
  );
};

export default memo(F1Leaderboard);