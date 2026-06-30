import React from 'react';
import { Box, Card, CardContent, Typography, Chip } from '@mui/material';
import { motion } from 'framer-motion';
import { Settings as SettingsIcon, Warning as WarningIcon, CheckCircle as CheckCircleIcon } from '@mui/icons-material';

const ServiceGap = ({ analysis, cleanedData }) => {
  // Extract services from data
  const allServices = cleanedData?.flatMap(c => c.services || []) || [];
  const serviceCounts = {};
  allServices.forEach(s => {
    serviceCounts[s] = (serviceCounts[s] || 0) + 1;
  });

  const commonServices = Object.entries(serviceCounts)
    .sort((a, b) => b[1] - a[1])
    .slice(0, 5)
    .map(([name]) => name);

  const rareServices = Object.entries(serviceCounts)
    .filter(([name, count]) => count === 1)
    .map(([name]) => name)
    .slice(0, 5);

  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.5 }}
    >
      <Card sx={{ p: 3, borderRadius: 3, height: '100%' }}>
        <Typography variant="h6" sx={{ fontWeight: 700, mb: 2 }}>
          <SettingsIcon sx={{ mr: 1, color: '#8b5cf6' }} />
          Service Gap Analysis
        </Typography>

        <Box mb={3}>
          <Typography variant="caption" sx={{ fontWeight: 600, color: '#22c55e' }}>
            <CheckCircleIcon sx={{ fontSize: 16, mr: 0.5, verticalAlign: 'middle' }} />
            Most Common Services
          </Typography>
          <Box display="flex" flexWrap="wrap" gap={0.5} sx={{ mt: 1 }}>
            {commonServices.map((service, i) => (
              <Chip key={i} label={service} size="small" sx={{ bgcolor: '#e8f5e9', color: '#2e7d32' }} />
            ))}
            {commonServices.length === 0 && (
              <Typography variant="body2" color="text.secondary">No common services found</Typography>
            )}
          </Box>
        </Box>

        <Box>
          <Typography variant="caption" sx={{ fontWeight: 600, color: '#f59e0b' }}>
            <WarningIcon sx={{ fontSize: 16, mr: 0.5, verticalAlign: 'middle' }} />
            Underserved Services
          </Typography>
          <Box display="flex" flexWrap="wrap" gap={0.5} sx={{ mt: 1 }}>
            {rareServices.map((service, i) => (
              <Chip key={i} label={service} size="small" variant="outlined" />
            ))}
            {rareServices.length === 0 && (
              <Typography variant="body2" color="text.secondary">No underserved services identified</Typography>
            )}
          </Box>
        </Box>
      </Card>
    </motion.div>
  );
};

export default ServiceGap;
