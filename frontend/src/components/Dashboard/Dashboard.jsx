import React from 'react';
import { Box, Grid, Typography, Container } from '@mui/material';
import { motion } from 'framer-motion';
import ExecutiveSummary from './ExecutiveSummary';
import KPICards from './KPICards';
import MarketOpportunities from './MarketOpportunities';
import TechnologyTrends from './TechnologyTrends';
import TechnologyGap from './TechnologyGap';
import ServiceGap from './ServiceGap';
import SWOTAnalysis from './SWOTAnalysis';
import RiskAnalysis from './RiskAnalysis';
import CompetitorBenchmark from './CompetitorBenchmark';
import StrategicRecommendations from './StrategicRecommendations';
import Roadmap from './Roadmap';
import AIInsights from './AIInsights';
import CompetitorDetails from './CompetitorDetails';
import IndustryAnalysis from './IndustryAnalysis';

const Dashboard = ({ analysis, cleanedData, techData, trendingTech, companyCount, totalTech }) => {
  // Loading state
  if (!analysis && !cleanedData) {
    return (
      <Box sx={{ p: 4, textAlign: 'center' }}>
        <Typography variant="h6" color="text.secondary">
          Run an analysis to view the dashboard
        </Typography>
      </Box>
    );
  }

  // Prepare data for sections
  const totalServices = analysis?.service_analysis?.total_services || 0;
  const totalClients = cleanedData?.reduce((acc, c) => acc + (c.clients?.names?.length || 0), 0) || 0;
  const totalProjects = cleanedData?.reduce((acc, c) => acc + (c.projects?.length || 0), 0) || 0;
  const industries = [...new Set(cleanedData?.flatMap(c => c.industry || []) || [])];
  const totalIndustries = industries.length;

  const kpiData = {
    companies: companyCount || 0,
    technologies: totalTech || 0,
    services: totalServices,
    clients: totalClients,
    industries: totalIndustries,
    projects: totalProjects
  };

  return (
    <motion.div
      initial={{ opacity: 0 }}
      animate={{ opacity: 1 }}
      transition={{ duration: 0.5 }}
    >
      <Container maxWidth="xl" sx={{ py: 3 }}>
        {/* Executive Summary */}
        <ExecutiveSummary 
          analysis={analysis} 
          cleanedData={cleanedData} 
          companyCount={companyCount} 
        />

        {/* KPI Cards */}
        <KPICards data={kpiData} />

        {/* Two Column Layout */}
        <Grid container spacing={3} sx={{ mt: 1 }}>
          <Grid item xs={12} md={6}>
            <MarketOpportunities analysis={analysis} cleanedData={cleanedData} />
          </Grid>
          <Grid item xs={12} md={6}>
            <RiskAnalysis analysis={analysis} cleanedData={cleanedData} />
          </Grid>
        </Grid>

        {/* Technology Trends */}
        <Box sx={{ mt: 3 }}>
          <TechnologyTrends 
            techData={techData} 
            trendingTech={trendingTech} 
            analysis={analysis} 
          />
        </Box>

        {/* Technology & Service Gap */}
        <Grid container spacing={3} sx={{ mt: 1 }}>
          <Grid item xs={12} md={6}>
            <TechnologyGap analysis={analysis} cleanedData={cleanedData} />
          </Grid>
          <Grid item xs={12} md={6}>
            <ServiceGap analysis={analysis} cleanedData={cleanedData} />
          </Grid>
        </Grid>

        {/* SWOT Analysis */}
        <Box sx={{ mt: 3 }}>
          <SWOTAnalysis analysis={analysis} cleanedData={cleanedData} />
        </Box>

        {/* Industry Analysis */}
        <Box sx={{ mt: 3 }}>
          <IndustryAnalysis 
            analysis={analysis} 
            cleanedData={cleanedData} 
            industries={industries}
          />
        </Box>

        {/* Competitor Benchmark */}
        <Box sx={{ mt: 3 }}>
          <CompetitorBenchmark cleanedData={cleanedData} />
        </Box>

        {/* Strategic Recommendations */}
        <Box sx={{ mt: 3 }}>
          <StrategicRecommendations analysis={analysis} cleanedData={cleanedData} />
        </Box>

        {/* Roadmap */}
        <Box sx={{ mt: 3 }}>
          <Roadmap analysis={analysis} cleanedData={cleanedData} />
        </Box>

        {/* AI Insights */}
        <Box sx={{ mt: 3 }}>
          <AIInsights analysis={analysis} cleanedData={cleanedData} />
        </Box>

        {/* Competitor Details */}
        <Box sx={{ mt: 3 }}>
          <CompetitorDetails cleanedData={cleanedData} />
        </Box>
      </Container>
    </motion.div>
  );
};

export default Dashboard;
