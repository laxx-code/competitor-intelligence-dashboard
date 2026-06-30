import React from 'react';
import { Box, Card, CardContent, Typography, Chip, Grid } from '@mui/material';
import { motion } from 'framer-motion';
import { Code as CodeIcon, Warning as WarningIcon, CheckCircle as CheckCircleIcon } from '@mui/icons-material';

const TechnologyGap = ({ analysis, cleanedData }) => {
  // Extract technologies from data
  const allTech = cleanedData?.flatMap(c => c.tech_stack || []) || [];
  const techCounts = {};
  allTech.forEach(t => {
    techCounts[t] = (techCounts[t] || 0) + 1;
  });

  const commonTech = Object.entries(techCounts)
    .sort((a, b) => b[1] - a[1])
    .slice(0, 5)
    .map(([name]) => name);

  const rareTech = Object.entries(techCounts)
    .filter(([name, count]) => count === 1)
    .map(([name]) => name)
    .slice(0, 5);

  const allTechList = Object.keys(techCounts);

  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.5 }}
    >
      <Card sx={{ p: 3, borderRadius: 3, height: '100%' }}>
        <Typography variant="h6" sx={{ fontWeight: 700, mb: 2 }}>
          <CodeIcon sx={{ mr: 1, color: '#6366f1' }} />
          Technology Gap Analysis
        </Typography>

        <Box mb={3}>
          <Typography variant="caption" sx={{ fontWeight: 600, color: '#22c55e' }}>
            <CheckCircleIcon sx={{ fontSize: 16, mr: 0.5, verticalAlign: 'middle' }} />
            Widely Used Technologies
          </Typography>
          <Box display="flex" flexWrap="wrap" gap={0.5} sx={{ mt: 1 }}>
            {commonTech.map((tech, i) => (
              <Chip key={i} label={tech} size="small" sx={{ bgcolor: '#e8f5e9', color: '#2e7d32' }} />
            ))}
            {commonTech.length === 0 && (
              <Typography variant="body2" color="text.secondary">No common technologies found</Typography>
            )}
          </Box>
        </Box>

        <Box mb={3}>
          <Typography variant="caption" sx={{ fontWeight: 600, color: '#f59e0b' }}>
            <WarningIcon sx={{ fontSize: 16, mr: 0.5, verticalAlign: 'middle' }} />
            Rare Technologies
          </Typography>
          <Box display="flex" flexWrap="wrap" gap={0.5} sx={{ mt: 1 }}>
            {rareTech.map((tech, i) => (
              <Chip key={i} label={tech} size="small" variant="outlined" />
            ))}
            {rareTech.length === 0 && (
              <Typography variant="body2" color="text.secondary">No rare technologies identified</Typography>
            )}
          </Box>
        </Box>

        <Box>
          <Typography variant="caption" sx={{ fontWeight: 600, color: '#6366f1' }}>
            Recommended Technologies to Adopt
          </Typography>
          <Box display="flex" flexWrap="wrap" gap={0.5} sx={{ mt: 1 }}>
            {commonTech.slice(0, 3).map((tech, i) => (
              <Chip key={i} label={tech} size="small" color="primary" />
            ))}
            {commonTech.length === 0 && (
              <Typography variant="body2" color="text.secondary">Run analysis to get recommendations</Typography>
            )}
          </Box>
        </Box>
      </Card>
    </motion.div>
  );
};

export default TechnologyGap;
