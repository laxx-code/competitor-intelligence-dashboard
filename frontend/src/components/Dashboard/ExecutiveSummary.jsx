import React from 'react';
import { Box, Card, CardContent, Typography, Chip, Grid } from '@mui/material';
import { motion } from 'framer-motion';
import { 
  TrendingUp as TrendingUpIcon,
  Business as BusinessIcon,
  Insights as InsightsIcon 
} from '@mui/icons-material';

const ExecutiveSummary = ({ analysis, cleanedData, companyCount }) => {
  const totalServices = analysis?.service_analysis?.total_services || 0;
  const totalTech = analysis?.technology_analysis?.total_technologies || 0;
  
  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.5 }}
    >
      <Card sx={{ 
        p: 3, 
        mb: 3, 
        borderRadius: 4,
        background: 'linear-gradient(135deg, #6366f1 0%, #8b5cf6 50%, #a855f7 100%)',
        color: 'white',
        position: 'relative',
        overflow: 'hidden'
      }}>
        <Box sx={{ position: 'relative', zIndex: 1 }}>
          <Box display="flex" alignItems="center" gap={1} mb={2}>
            <InsightsIcon />
            <Typography variant="h5" sx={{ fontWeight: 700 }}>
              Executive Summary
            </Typography>
            <Chip 
              label={`${companyCount} Companies Analyzed`} 
              size="small" 
              sx={{ 
                bgcolor: 'rgba(255,255,255,0.2)', 
                color: 'white',
                ml: 2
              }} 
            />
          </Box>

          <Grid container spacing={3}>
            <Grid item xs={12} md={8}>
              <Typography variant="body1" sx={{ opacity: 0.9, lineHeight: 1.8 }}>
                Analysis of {companyCount} competitor companies reveals a dynamic market with 
                {totalServices > 0 ? ` ${totalServices} unique services` : ''} 
                {totalTech > 0 ? ` and ${totalTech} technologies` : ''}. 
                {companyCount > 0 ? ` The competitive landscape shows ${companyCount > 3 ? 'significant competition' : 'emerging opportunities'} in this space.` : ' Run an analysis to generate insights.'}
              </Typography>
            </Grid>
            <Grid item xs={12} md={4}>
              <Box 
                sx={{ 
                  p: 2, 
                  bgcolor: 'rgba(255,255,255,0.1)', 
                  borderRadius: 2,
                  backdropFilter: 'blur(8px)'
                }}
              >
                <Typography variant="caption" sx={{ opacity: 0.8 }}>
                  Key Findings
                </Typography>
                <Box mt={1}>
                  <Box display="flex" alignItems="center" gap={1} mb={1}>
                    <TrendingUpIcon sx={{ fontSize: 16 }} />
                    <Typography variant="body2">
                      {totalServices > 5 ? 'Diverse service offerings' : 'Service portfolio expansion opportunity'}
                    </Typography>
                  </Box>
                  <Box display="flex" alignItems="center" gap={1}>
                    <BusinessIcon sx={{ fontSize: 16 }} />
                    <Typography variant="body2">
                      {companyCount > 0 ? `${companyCount} active competitors` : 'No competitors analyzed'}
                    </Typography>
                  </Box>
                </Box>
              </Box>
            </Grid>
          </Grid>
        </Box>
      </Card>
    </motion.div>
  );
};

export default ExecutiveSummary;
