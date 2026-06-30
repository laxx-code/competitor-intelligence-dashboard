import React from 'react';
import { Box, Card, CardContent, Typography, Grid } from '@mui/material';
import { motion } from 'framer-motion';
import {
  TrendingUp as TrendingUpIcon,
  TrendingDown as TrendingDownIcon,
  Lightbulb as LightbulbIcon,
  Warning as WarningIcon
} from '@mui/icons-material';

const SWOTCard = ({ title, items, icon, color, bgColor }) => {
  return (
    <motion.div
      whileHover={{ y: -4, transition: { duration: 0.2 } }}
      style={{ height: '100%' }}
    >
      <Card sx={{ 
        p: 2, 
        borderRadius: 3, 
        bgcolor: bgColor,
        border: `1px solid ${color}30`,
        height: '100%'
      }}>
        <Box display="flex" alignItems="center" gap={1} mb={1}>
          {icon}
          <Typography variant="subtitle2" sx={{ fontWeight: 700, color: color }}>
            {title}
          </Typography>
        </Box>
        {(items || []).map((item, index) => (
          <Typography key={index} variant="body2" sx={{ py: 0.5, color: '#475569' }}>
            • {item}
          </Typography>
        ))}
        {(!items || items.length === 0) && (
          <Typography variant="body2" color="text.secondary" sx={{ py: 1 }}>
            No data available
          </Typography>
        )}
      </Card>
    </motion.div>
  );
};

const SWOTAnalysis = ({ analysis, cleanedData }) => {
  // Generate SWOT items from data
  const allServices = cleanedData?.flatMap(c => c.services || []) || [];
  const allTech = cleanedData?.flatMap(c => c.tech_stack || []) || [];
  const allClients = cleanedData?.flatMap(c => c.clients?.names || []) || [];
  
  const strengths = [
    `${allServices.length > 0 ? `${allServices.length} services offered` : 'Limited service offerings'}`,
    `${allTech.length > 0 ? `${allTech.length} technologies used` : 'Limited technology adoption'}`,
    `${allClients.length > 0 ? `${allClients.length} clients served` : 'Client base growing'}`
  ].filter(s => s);

  const weaknesses = [
    `${allServices.length < 3 ? 'Limited service portfolio' : 'Moderate service diversity'}`,
    `${allTech.length < 3 ? 'Limited technology stack' : 'Technology adoption ongoing'}`,
    `${cleanedData?.length > 0 ? 'Competition in market' : 'Market presence developing'}`
  ];

  const opportunities = [
    'Expand service offerings',
    'Adopt emerging technologies',
    'Enter new markets',
    'Build strategic partnerships'
  ];

  const threats = [
    `${cleanedData?.length > 3 ? 'High competition' : 'Growing competition'}`,
    'Technology disruption',
    'Market saturation',
    'Talent acquisition challenges'
  ];

  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.5 }}
    >
      <Typography variant="h6" sx={{ fontWeight: 700, mb: 2 }}>
        SWOT Analysis
      </Typography>

      <Grid container spacing={2}>
        <Grid item xs={12} sm={6} md={3}>
          <SWOTCard
            title="Strengths"
            items={strengths}
            icon={<TrendingUpIcon sx={{ color: '#22c55e' }} />}
            color="#22c55e"
            bgColor="#f0fdf4"
          />
        </Grid>
        <Grid item xs={12} sm={6} md={3}>
          <SWOTCard
            title="Weaknesses"
            items={weaknesses}
            icon={<TrendingDownIcon sx={{ color: '#ef4444' }} />}
            color="#ef4444"
            bgColor="#fef2f2"
          />
        </Grid>
        <Grid item xs={12} sm={6} md={3}>
          <SWOTCard
            title="Opportunities"
            items={opportunities}
            icon={<LightbulbIcon sx={{ color: '#3b82f6' }} />}
            color="#3b82f6"
            bgColor="#eff6ff"
          />
        </Grid>
        <Grid item xs={12} sm={6} md={3}>
          <SWOTCard
            title="Threats"
            items={threats}
            icon={<WarningIcon sx={{ color: '#f59e0b' }} />}
            color="#f59e0b"
            bgColor="#fefce8"
          />
        </Grid>
      </Grid>
    </motion.div>
  );
};

export default SWOTAnalysis;
