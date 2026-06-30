import React from 'react';
import { Box, Card, CardContent, Typography, Chip, Grid, LinearProgress } from '@mui/material';
import { motion } from 'framer-motion';
import { TrendingUp as TrendingUpIcon } from '@mui/icons-material';

const CompetitorCard = ({ company, rank }) => {
  const services = company.services?.length || 0;
  const tech = company.tech_stack?.length || 0;
  const clients = company.clients?.names?.length || 0;
  const projects = company.projects?.length || 0;
  
  const scores = {
    innovation: Math.min(100, tech * 15 + 20),
    technology: Math.min(100, tech * 12 + 20),
    market: Math.min(100, clients * 10 + 20),
    service: Math.min(100, services * 10 + 20)
  };
  const overall = Math.round((scores.innovation + scores.technology + scores.market + scores.service) / 4);

  return (
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
        <Box display="flex" justifyContent="space-between" alignItems="center" mb={2}>
          <Box display="flex" alignItems="center" gap={1}>
            <Box 
              sx={{ 
                width: 32, 
                height: 32, 
                borderRadius: '50%', 
                bgcolor: '#6366f1',
                display: 'flex',
                alignItems: 'center',
                justifyContent: 'center',
                color: 'white',
                fontWeight: 'bold',
                fontSize: '14px'
              }}
            >
              {company.company?.charAt(0) || '?'}
            </Box>
            <Box>
              <Typography variant="subtitle2" sx={{ fontWeight: 600 }}>
                {company.company || 'Unknown'}
              </Typography>
              <Typography variant="caption" color="text.secondary" sx={{ fontSize: '10px' }}>
                {company.url || ''}
              </Typography>
            </Box>
          </Box>
          <Chip 
            label={`#${rank + 1}`} 
            size="small" 
            sx={{ bgcolor: '#6366f1', color: 'white', fontWeight: 600 }} 
          />
        </Box>

        <Box display="flex" gap={1} flexWrap="wrap" mb={2}>
          <Chip label={`${services} Services`} size="small" variant="outlined" />
          <Chip label={`${tech} Tech`} size="small" variant="outlined" />
          <Chip label={`${clients} Clients`} size="small" variant="outlined" />
          <Chip label={`${projects} Projects`} size="small" variant="outlined" />
        </Box>

        <Box>
          <Box display="flex" alignItems="center" gap={1} mb={0.5}>
            <Typography variant="caption" color="text.secondary">Overall Score</Typography>
            <Chip 
              label={overall} 
              size="small" 
              sx={{ 
                bgcolor: overall >= 70 ? '#22c55e' : overall >= 50 ? '#f59e0b' : '#ef4444',
                color: 'white',
                fontWeight: 700,
                height: 20,
                fontSize: '11px'
              }} 
            />
          </Box>
          <LinearProgress 
            variant="determinate" 
            value={overall} 
            sx={{ 
              height: 6, 
              borderRadius: 3,
              bgcolor: '#e2e8f0',
              '& .MuiLinearProgress-bar': {
                borderRadius: 3,
                bgcolor: overall >= 70 ? '#22c55e' : overall >= 50 ? '#f59e0b' : '#ef4444'
              }
            }} 
          />
        </Box>
      </Card>
    </motion.div>
  );
};

const CompetitorBenchmark = ({ cleanedData }) => {
  if (!cleanedData || cleanedData.length === 0) {
    return (
      <Card sx={{ p: 4, textAlign: 'center', borderRadius: 3 }}>
        <Typography variant="h6" color="text.secondary">
          No competitor data available
        </Typography>
      </Card>
    );
  }

  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.5 }}
    >
      <Typography variant="h6" sx={{ fontWeight: 700, mb: 2 }}>
        <TrendingUpIcon sx={{ mr: 1, color: '#6366f1' }} />
        Competitor Benchmark
      </Typography>

      <Grid container spacing={2}>
        {cleanedData.map((company, index) => (
          <Grid item xs={12} sm={6} md={4} key={index}>
            <CompetitorCard company={company} rank={index} />
          </Grid>
        ))}
      </Grid>
    </motion.div>
  );
};

export default CompetitorBenchmark;
