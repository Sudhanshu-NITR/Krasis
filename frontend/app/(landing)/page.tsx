import AppPreview from "@/components/landing/AppPreview";
import Architecture from "@/components/landing/Architecture";
import CallToAction from "@/components/landing/CallToAction";
import HeroSection from "@/components/landing/HeroSection";
import IntegrationsBanner from "@/components/landing/IntegrationsBanner";

export default function page() {
  return (
    <div className="min-h-screen bg-black text-white font-sans selection:bg-indigo-500/30 overflow-x-hidden">
        <HeroSection />
        <AppPreview />
        <Architecture />
        <IntegrationsBanner />
        <CallToAction />
    </div>
  )
}
