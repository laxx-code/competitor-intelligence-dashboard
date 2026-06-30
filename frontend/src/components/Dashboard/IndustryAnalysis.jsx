import React from 'react';
import { Box, Card, CardContent, Typography, Chip, Grid } from '@mui/material';
import { motion } from 'framer-motion';
import { 
  AccountTree as AccountTreeIcon,
  PieChart as PieChartIcon 
} from '@mui/icons-material';
import { PieChart, Pie, Cell, ResponsiveContainer, Tooltip } from 'recharts';

const IndustryAnalysis = ({ analysis, cleanedData, industries }) => {
  const industryData = (industries || []).map(ind => ({
    name: ind,
    value: cleanedData?.filter(c => (c.industry || []).includes(ind)).length || 0
  }));

  const COLORS = ['#6366f1', '#8b5cf6', '#a855f7', '#d946ef', '#ec4899', '#f43f5e', '#fb7185', '#f472b6'];
  const topIndustries = industryData.sort((a, b) => b.value - a.value).slice(0, 5);

  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.5 }}
    >
      <Typography variant="h6" sx={{ fontWeight: 700, mb: 2 }}>
        <AccountTreeIcon sx={{ mr: 1, color: '#8b5cf6' }} />
        Industry Analysis
      </Typography>

      <Grid container spacing={3}>
        <Grid item xs={12} md={6}>
          <Card sx={{ p: 3, borderRadius: 3, height: '100%' }}>
            <Typography variant="subtitle2" sx={{ fontWeight: 600, mb: 2 }}>
              Industry Distribution
            </Typography>
            {industryData.length > 0 ? (
              <ResponsiveContainer width="100%" height={250}>
                <PieChart>
                  <Pie
                    data={industryData}
                    cx="50%"
                    cy="50%"
                    labelLine={false}
                    label={({ name, percent }) => `${name} (${(percent * 100).toFixed(0)}%)`}
                    outerRadius={80}
                    dataKey="value"
                  >
                    {industryData.map((entry, index) => (
                      <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
                    ))}
                  </Pie>
                  <Tooltip />
                </PieChart>
              </ResponsiveContainer>
            ) : (
              <Typography variant="body2" color="text.secondary" sx={{ textAlign: 'center', py: 4 }}>
                No industry data available
              </Typography>
            )}
          </Card>
        </Grid>

        <Grid item xs={12} md={6}>
          <Card sx={{ p: 3, borderRadius: 3, height: '100%' }}>
            <Typography variant="subtitle2" sx={{ fontWeight: 600, mb: 2 }}>
              Top Industries
            </Typography>
            {topIndustries.map((ind, index) => (
              <Box 
                key={index} 
                sx={{ 
                  display: 'flex', 
                  alignItems: 'center', 
                  justifyContent: 'space-between', 
                  py: 1,
                  borderBottom: index < topIndustries.length - 1 ? '1px solid #e2e8f0' : 'none'
                }}
              >
                <Box display="flex" alignItems="center" gap={1}>
                  <Box sx={{ 
                    width: 8, 
                    height: 8, 
                    borderRadius: '50%', 
                    bgcolor: COLORS[index % COLORS.length] 
                  }} />
                  <Typography variant="body2">{ind.name}</Typography>
                </Box>
                <Chip 
                  label={`${ind.value} companies`} 
                  size="small" 
                  sx={{ bgcolor: '#6366f1', color: 'white', height: 20, fontSize: '10px' }} 
                />
              </Box>
            ))}
            {topIndustries.length === 0 && (
              <Typography variant="body2" color="text.secondary" sx={{ textAlign: 'center', py: 2 }}>
                No industry data available
              </Typography>
            )}
          </Card>
        </Grid>
      </Grid>
    </motion.div>
  );
};

export default IndustryAnalysis;
