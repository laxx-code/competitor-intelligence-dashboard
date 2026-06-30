import React from 'react';
import { Box, Card, CardContent, Typography, Chip, Grid } from '@mui/material';
import { motion } from 'framer-motion';
import { 
  Lightbulb as LightbulbIcon, 
  TrendingUp as TrendingUpIcon,
  Warning as WarningIcon,
  Insights as InsightsIcon
} from '@mui/icons-material';

const AIInsights = ({ analysis, cleanedData }) => {
  const allServices = cleanedData?.flatMap(c => c.services || []) || [];
  const allTech = cleanedData?.flatMap(c => c.tech_stack || []) || [];
  const totalCompanies = cleanedData?.length || 0;

  const insights = [
    {
      title: 'Competitive Landscape',
      description: `${totalCompanies} competitors identified in the market`,
      category: 'Market Analysis',
      priority: 'High',
      confidence: 90,
      action: 'Review competitor strategies',
      icon: <InsightsIcon />
    },
    {
      title: 'Service Gaps Identified',
      description: `${allServices.length} total services offered by competitors`,
      category: 'Opportunity',
      priority: 'High',
      confidence: 85,
      action: 'Develop new service offerings',
      icon: <LightbulbIcon />
    },
    {
      title: 'Technology Adoption Trends',
      description: `${allTech.length} technologies used across competitors`,
      category: 'Trend',
      priority: 'Medium',
      confidence: 80,
      action: 'Adopt key technologies',
      icon: <TrendingUpIcon />
    },
    {
      title: 'Market Opportunities',
      description: `${totalCompanies > 3 ? 'High competition market' : 'Growing market with opportunities'}`,
      category: 'Strategy',
      priority: 'High',
      confidence: 75,
      action: 'Differentiate and capture market share',
      icon: <LightbulbIcon />
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
      <Typography variant="h6" sx={{ fontWeight: 700, mb: 2 }}>
        <InsightsIcon sx={{ mr: 1, color: '#f59e0b' }} />
        AI Insights
      </Typography>

      <Grid container spacing={2}>
        {insights.map((insight, index) => (
          <Grid item xs={12} md={6} key={index}>
            <motion.div
              whileHover={{ y: -4, transition: { duration: 0.2 } }}
            >
              <Card sx={{ 
                p: 2, 
                borderRadius: 3,
                border: '1px solid #e2e8f0',
                height: '100%',
                '&:hover': {
                  boxShadow: '0 8px 32px rgba(0,0,0,0.08)'
                }
              }}>
                <Box display="flex" alignItems="flex-start" gap={1}>
                  <Box sx={{ 
                    p: 0.5, 
                    bgcolor: 'rgba(99,102,241,0.1)', 
                    borderRadius: 1,
                    color: '#6366f1'
                  }}>
                    {insight.icon}
                  </Box>
                  <Box flex={1}>
                    <Box display="flex" justifyContent="space-between" alignItems="center" flexWrap="wrap">
                      <Typography variant="subtitle2" sx={{ fontWeight: 600 }}>
                        {insight.title}
                      </Typography>
                      <Box display="flex" gap={0.5}>
                        <Chip 
                          label={insight.category} 
                          size="small" 
                          sx={{ height: 18, fontSize: '9px' }} 
                        />
                        <Chip 
                          label={insight.priority} 
                          size="small" 
                          sx={{ 
                            bgcolor: `${getPriorityColor(insight.priority)}20`, 
                            color: getPriorityColor(insight.priority),
                            height: 18,
                            fontSize: '9px',
                            fontWeight: 600
                          }} 
                        />
                        <Chip 
                          label={`${insight.confidence}%`} 
                          size="small" 
                          sx={{ bgcolor: 'rgba(99,102,241,0.1)', color: '#6366f1', height: 18, fontSize: '9px' }} 
                        />
                      </Box>
                    </Box>
                    <Typography variant="body2" color="text.secondary" sx={{ mt: 0.5 }}>
                      {insight.description}
                    </Typography>
                    <Typography variant="caption" color="primary" display="block" sx={{ mt: 0.5 }}>
                      Action: {insight.action}
                    </Typography>
                  </Box>
                </Box>
              </Card>
            </motion.div>
          </Grid>
        ))}
      </Grid>
    </motion.div>
  );
};

export default AIInsights;
