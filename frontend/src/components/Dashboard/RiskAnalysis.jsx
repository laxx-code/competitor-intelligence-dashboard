import React from 'react';
import { Box, Card, CardContent, Typography, Chip, Grid } from '@mui/material';
import { motion } from 'framer-motion';
import { Warning as WarningIcon, Error as ErrorIcon, Info as InfoIcon } from '@mui/icons-material';

const RiskAnalysis = ({ analysis, cleanedData }) => {
  const allClients = cleanedData?.flatMap(c => c.clients?.names || []) || [];
  const clientCounts = {};
  allClients.forEach(c => {
    clientCounts[c] = (clientCounts[c] || 0) + 1;
  });
  
  const sharedClients = Object.entries(clientCounts)
    .filter(([name, count]) => count > 1)
    .map(([name]) => name);

  const risks = [
    {
      title: 'Client Concentration Risk',
      description: `${sharedClients.length} clients are shared across multiple competitors`,
      severity: sharedClients.length > 2 ? 'High' : 'Medium',
      impact: 'Medium',
      recommendation: sharedClients.length > 0 ? 'Differentiate service offerings to reduce overlap' : 'Build unique value proposition'
    },
    {
      title: 'Technology Dependency',
      description: `${cleanedData?.length || 0} competitors may rely on similar technology stacks`,
      severity: 'Medium',
      impact: 'Low',
      recommendation: 'Adopt emerging technologies to gain advantage'
    },
    {
      title: 'Market Saturation',
      description: `${cleanedData?.length || 0} competitors in the market`,
      severity: cleanedData?.length > 3 ? 'High' : 'Low',
      impact: 'Medium',
      recommendation: cleanedData?.length > 3 ? 'Differentiate or expand to new markets' : 'Capture market share early'
    }
  ];

  const getSeverityColor = (severity) => {
    switch(severity?.toLowerCase()) {
      case 'high': return '#ef4444';
      case 'medium': return '#f59e0b';
      case 'low': return '#22c55e';
      default: return '#6366f1';
    }
  };

  const getSeverityIcon = (severity) => {
    switch(severity?.toLowerCase()) {
      case 'high': return <ErrorIcon sx={{ fontSize: 16, color: '#ef4444' }} />;
      case 'medium': return <WarningIcon sx={{ fontSize: 16, color: '#f59e0b' }} />;
      default: return <InfoIcon sx={{ fontSize: 16, color: '#22c55e' }} />;
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
          <WarningIcon sx={{ mr: 1, color: '#ef4444' }} />
          Competitive Risk Analysis
        </Typography>

        {risks.map((risk, index) => (
          <Box 
            key={index} 
            sx={{ 
              p: 2, 
              mb: 2, 
              borderRadius: 2, 
              bgcolor: '#f8fafc',
              borderLeft: `4px solid ${getSeverityColor(risk.severity)}`,
              '&:last-child': { mb: 0 }
            }}
          >
            <Box display="flex" justifyContent="space-between" alignItems="center" flexWrap="wrap">
              <Box display="flex" alignItems="center" gap={1}>
                {getSeverityIcon(risk.severity)}
                <Typography variant="subtitle2" sx={{ fontWeight: 600 }}>
                  {risk.title}
                </Typography>
              </Box>
              <Box display="flex" gap={1}>
                <Chip 
                  label={risk.severity} 
                  size="small" 
                  sx={{ 
                    bgcolor: `${getSeverityColor(risk.severity)}20`, 
                    color: getSeverityColor(risk.severity),
                    fontWeight: 600
                  }} 
                />
                <Chip 
                  label={`Impact: ${risk.impact}`} 
                  size="small" 
                  variant="outlined"
                />
              </Box>
            </Box>
            <Typography variant="body2" color="text.secondary" sx={{ mt: 1 }}>
              {risk.description}
            </Typography>
            <Typography variant="caption" color="primary" display="block" sx={{ mt: 1 }}>
              Recommendation: {risk.recommendation}
            </Typography>
          </Box>
        ))}
      </Card>
    </motion.div>
  );
};

export default RiskAnalysis;
