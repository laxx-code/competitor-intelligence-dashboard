import React from 'react';
import { Box, Card, CardContent, Typography, Chip } from '@mui/material';
import { motion } from 'framer-motion';
import { TrendingUp as TrendingUpIcon, Lightbulb as LightbulbIcon } from '@mui/icons-material';

const MarketOpportunities = ({ analysis, cleanedData }) => {
  const allServices = cleanedData?.flatMap(c => c.services || []) || [];
  const serviceCounts = {};
  allServices.forEach(s => {
    serviceCounts[s] = (serviceCounts[s] || 0) + 1;
  });

  const rareServices = Object.entries(serviceCounts)
    .filter(([name, count]) => count === 1)
    .map(([name]) => name)
    .slice(0, 3);

  const opportunities = [
    {
      title: 'Service Portfolio Expansion',
      description: `${rareServices.length > 0 ? `Opportunities in: ${rareServices.join(', ')}` : 'Differentiate with unique services'}`,
      impact: 'High',
      priority: 'High',
      confidence: 80,
      reasoning: `Based on ${cleanedData?.length || 0} competitors analyzed`
    },
    {
      title: 'Market Positioning',
      description: `Position as a ${cleanedData?.length > 3 ? 'specialized' : 'full-service'} provider`,
      impact: 'Medium',
      priority: 'High',
      confidence: 75,
      reasoning: 'Differentiation strategy based on competitor analysis'
    },
    {
      title: 'Client Acquisition',
      description: `Target ${cleanedData?.length > 0 ? 'underserved industries' : 'early adopters'}`,
      impact: 'High',
      priority: 'Medium',
      confidence: 70,
      reasoning: 'Identified through client gap analysis'
    }
  ];

  const getPriorityColor = (priority) => {
    switch(priority?.toLowerCase()) {
      case 'high': return '#ef4444';
      case 'medium': return '#f59e0b';
      default: return '#22c55e';
    }
  };

  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.5 }}
    >
      <Card sx={{ p: 3, borderRadius: 3, height: '100%' }}>
        <Typography variant="h6" sx={{ fontWeight: 700, mb: 2 }}>
          <LightbulbIcon sx={{ mr: 1, color: '#22c55e' }} />
          Market Opportunities
        </Typography>

        {opportunities.map((opp, index) => (
          <Box 
            key={index} 
            sx={{ 
              p: 2, 
              mb: 2, 
              borderRadius: 2, 
              bgcolor: '#f8fafc',
              '&:last-child': { mb: 0 }
            }}
          >
            <Box display="flex" justifyContent="space-between" alignItems="center" flexWrap="wrap">
              <Typography variant="subtitle2" sx={{ fontWeight: 600 }}>
                {opp.title}
              </Typography>
              <Box display="flex" gap={1}>
                <Chip 
                  label={opp.priority} 
                  size="small" 
                  sx={{ 
                    bgcolor: `${getPriorityColor(opp.priority)}20`, 
                    color: getPriorityColor(opp.priority),
                    fontWeight: 600
                  }} 
                />
                <Chip 
                  label={`${opp.confidence}% confidence`} 
                  size="small" 
                  sx={{ bgcolor: 'rgba(99,102,241,0.1)', color: '#6366f1' }} 
                />
                <Chip 
                  label={opp.impact} 
                  size="small" 
                  variant="outlined"
                />
              </Box>
            </Box>
            <Typography variant="body2" color="text.secondary" sx={{ mt: 1 }}>
              {opp.description}
            </Typography>
            <Typography variant="caption" color="text.secondary" display="block" sx={{ mt: 0.5 }}>
              Reasoning: {opp.reasoning}
            </Typography>
          </Box>
        ))}
      </Card>
    </motion.div>
  );
};

export default MarketOpportunities;
