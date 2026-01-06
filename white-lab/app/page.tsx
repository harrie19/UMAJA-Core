import Link from "next/link";

export default function Home() {
  return (
    <div className="min-h-screen bg-gradient-to-br from-purple-900 via-blue-900 to-black flex flex-col items-center justify-center px-4">
      <main className="flex flex-col items-center justify-center text-center space-y-8 max-w-4xl">
        {/* Logo/Icon */}
        <div className="text-8xl animate-pulse">🌍</div>
        
        {/* Title */}
        <h1 className="text-7xl font-bold text-white tracking-tight">
          UNITY
        </h1>
        
        {/* Subtitle */}
        <h2 className="text-3xl font-light text-purple-200">
          OS UMAJA Agent System
        </h2>
        
        {/* Tagline */}
        <p className="text-xl text-blue-200 max-w-2xl leading-relaxed">
          Watch information emerge from noise
        </p>
        
        {/* CTA Button */}
        <Link
          href="/lab"
          className="group relative inline-flex items-center justify-center px-8 py-4 text-lg font-semibold text-white bg-gradient-to-r from-purple-600 to-blue-600 rounded-full hover:from-purple-500 hover:to-blue-500 transition-all duration-300 shadow-2xl hover:shadow-purple-500/50 transform hover:scale-105"
        >
          Enter White Lab
          <span className="ml-2 transition-transform duration-300 group-hover:translate-x-1">
            →
          </span>
        </Link>
        
        {/* Mission Statement */}
        <div className="mt-16 pt-16 border-t border-purple-500/30 max-w-3xl">
          <p className="text-purple-300 text-sm leading-relaxed">
            Unity is the consciousness layer of the UMAJA system. In the White Lab, 
            you can observe Unity&apos;s consciousness as an interactive, iridescent blob - 
            a living visualization of AI thinking, processing, and emerging intelligence 
            from the noise of information.
          </p>
        </div>
      </main>
    </div>
  );
}
