'use client';

export default function IntegrationsBanner() {
    return (
        <section className="py-24 border-y border-white/5 bg-white/2">
            <div className="max-w-7xl mx-auto px-6 text-center">
                <p className="text-sm font-medium text-zinc-500 uppercase tracking-widest mb-8">Pattern Adopted By Engineering Teams At</p>
                <div className="flex flex-wrap justify-center gap-12 md:gap-20 opacity-50 grayscale hover:grayscale-0 transition-all duration-500">
                    <span className="text-2xl font-bold text-white flex items-center gap-2"><div className="w-6 h-6 bg-white rounded-full"></div>Stripe</span>
                    <span className="text-2xl font-bold text-white flex items-center gap-2"><div className="w-6 h-6 bg-white rounded-sm"></div>Uber</span>
                    <span className="text-2xl font-bold text-white flex items-center gap-2"><div className="w-6 h-6 bg-white rounded-full"></div>Twilio</span>
                    <span className="text-2xl font-bold text-white flex items-center gap-2"><div className="w-6 h-6 bg-white rounded-md"></div>MongoDB</span>
                </div>
            </div>
        </section>
    )
}
