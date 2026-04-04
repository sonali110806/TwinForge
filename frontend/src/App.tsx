import { QueryClient, QueryClientProvider } from "@tanstack/react-query";
import { BrowserRouter, Route, Routes } from "react-router-dom";
import { Toaster as Sonner } from "@/components/ui/sonner";
import { Toaster } from "@/components/ui/toaster";
import { TooltipProvider } from "@/components/ui/tooltip";
import DashboardLayout from "@/components/twinforge/DashboardLayout";
import Index from "./pages/Index.tsx";
import TwinsPage from "./pages/TwinsPage.tsx";
import AIReasoningPage from "./pages/AIReasoningPage.tsx";
import TournamentPage from "./pages/TournamentPage.tsx";
import DeployPage from "./pages/DeployPage.tsx";
import LogsPage from "./pages/LogsPage.tsx";
import ReportsPage from "./pages/ReportsPage.tsx";
import SettingsPage from "./pages/SettingsPage.tsx";
import NotFound from "./pages/NotFound.tsx";

const queryClient = new QueryClient();

const App = () => (
  <QueryClientProvider client={queryClient}>
    <TooltipProvider>
      <Toaster />
      <Sonner />
      <BrowserRouter>
        <Routes>
          <Route element={<DashboardLayout />}>
            <Route path="/" element={<Index />} />
            <Route path="/twins" element={<TwinsPage />} />
            <Route path="/ai" element={<AIReasoningPage />} />
            <Route path="/tournament" element={<TournamentPage />} />
            <Route path="/deploy" element={<DeployPage />} />
            <Route path="/logs" element={<LogsPage />} />
            <Route path="/reports" element={<ReportsPage />} />
            <Route path="/settings" element={<SettingsPage />} />
          </Route>
          <Route path="*" element={<NotFound />} />
        </Routes>
      </BrowserRouter>
    </TooltipProvider>
  </QueryClientProvider>
);

export default App;
