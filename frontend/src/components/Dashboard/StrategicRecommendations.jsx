import React from 'react';
import { Box, Card, CardContent, Typography, Chip, Grid } from '@mui/material';
import { motion } from 'framer-motion';
import { TrendingUp as TrendingUpIcon } from '@mui/icons-material';

const StrategicRecommendations = ({ analysis, cleanedData }) => {
  const allServices = cleanedData?.flatMap(c => c.services || []) || [];
  const allTech = cleanedData?.flatMap(c => c.tech_stack || []) || [];

  const recommendations = [
    {
      title: 'Adopt Emerging Technologies',
      reason: `${allTech.length} technologies identified across competitors`,
      impact: 'High',
      priority: 'High',
      effort: 'Medium',
      description: `Focus on ${allTech.slice(0, 3).join(', ') || 'AI and cloud technologies'} to stay competitive`
    },
    {
      title: 'Expand Service Portfolio',
      reason: `${allServices.length} services offered by competitors`,
      impact: 'High',
      priority: 'Medium',
      effort: 'High',
      description: `Add services similar to ${allServices.slice(0, 3).join(', ') || 'high-demand offerings'}`
    },
    {
      title: 'Strengthen Client Relationships',
      reason: `Build on existing client base and target new segments`,
      impact: 'Medium',
      priority: 'High',
      effort: 'Low',
      description: 'Improve client retention and acquisition strategies'
    },
    {
      title: 'Optimize Technology Stack',
      reason: 'Reduce technical debt and improve scalability',
      impact: 'Medium',
      priority: 'Medium',
      effort: 'High',
      description: 'Modernize technology stack for better performance'
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
        <TrendingUpIcon sx={{ mr: 1, color: '#8b5cf6' }} />
        Strategic Recommendations
      </Typography>

      <Grid container spacing={2}>
        {recommendations.map((rec, index) => (
          <Grid item xs={12} md={6} key={index}>
            <motion.div
              whileHover={{ y: -4, transition: { duration: 0.2 } }}
            >
              <Card sx={{ p: 2, borderRadius: 3, height: '100%' }}>
                <Box display="flex" justifyContent="space-between" alignItems="center" flexWrap="wrap">
                  <Typography variant="subtitle2" sx={{ fontWeight: 600 }}>
                    {rec.title}
                  </Typography>
                  <Box display="flex" gap={0.5}>
                    <Chip 
                      label={rec.priority} 
                      size="small" 
                      sx={{ 
                        bgcolor: `${getPriorityColor(rec.priority)}20`, 
                        color: getPriorityColor(rec.priority),
                        fontWeight: 600,
                        height: 20,
                        fontSize: '10px'
                      }} 
                    />
                    <Chip 
                      label={`Effort: ${rec.effort}`} 
                      size="small" 
                      variant="outlined"
                      sx={{ height: 20, fontSize: '10px' }}
                    />
                  </Box>
                </Box>
                <Typography variant="body2" color="text.secondary" sx={{ mt: 1 }}>
                  {rec.description}
                </Typography>
                <Box display="flex" gap={1} sx={{ mt: 1 }}>
                  <Chip 
                    label={`Impact: ${rec.impact}`} 
                    size="small" 
                    sx={{ bgcolor: 'rgba(99,102,241,0.1)', color: '#6366f1', height: 20, fontSize: '10px' }} 
                  />
                  <Chip 
                    label={rec.reason} 
                    size="small" 
                    variant="outlined"
                    sx={{ height: 20, fontSize: '10px' }}
                  />
                </Box>
              </Card>
            </motion.div>
          </Grid>
        ))}
      </Grid>
    </motion.div>
  );
};

export default StrategicRecommendations;
