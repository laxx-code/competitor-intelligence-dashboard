import React from 'react';
import { Box, Card, CardContent, Typography, Chip, Grid } from '@mui/material';
import { motion } from 'framer-motion';
import {
  BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer, Cell
} from 'recharts';
import { Whatshot as WhatshotIcon, TrendingUp as TrendingUpIcon } from '@mui/icons-material';

const TechnologyTrends = ({ techData, trendingTech, analysis }) => {
  const COLORS = ['#6366f1', '#8b5cf6', '#a855f7', '#d946ef', '#ec4899', '#f43f5e', '#fb7185', '#f472b6'];

  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.5 }}
    >
      <Typography variant="h6" sx={{ fontWeight: 700, mb: 2 }}>
        <TrendingUpIcon sx={{ mr: 1, color: '#6366f1' }} />
        Technology Trends
      </Typography>

      <Grid container spacing={3}>
        <Grid item xs={12} md={8}>
          <Card sx={{ p: 3, borderRadius: 3 }}>
            <Typography variant="subtitle2" sx={{ fontWeight: 600, mb: 2 }}>
              Technology Stack Distribution
            </Typography>
            <ResponsiveContainer width="100%" height={280}>
              <BarChart data={techData || []} margin={{ top: 10, right: 20, left: 0, bottom: 40 }}>
                <CartesianGrid strokeDasharray="3 3" stroke="#e2e8f0" />
                <XAxis dataKey="name" angle={-45} textAnchor="end" height={60} fontSize={11} />
                <YAxis fontSize={11} />
                <Tooltip />
                <Legend />
                <Bar dataKey="value" name="Companies">
                  {(techData || []).map((entry, index) => (
                    <Cell key={`cell-${index}`} fill={entry.fill || COLORS[index % COLORS.length]} />
                  ))}
                </Bar>
              </BarChart>
            </ResponsiveContainer>
          </Card>
        </Grid>

        <Grid item xs={12} md={4}>
          <Card sx={{ p: 3, borderRadius: 3, height: '100%' }}>
            <Typography variant="subtitle2" sx={{ fontWeight: 600, mb: 2 }}>
              <WhatshotIcon sx={{ mr: 1, color: '#ef4444' }} />
              Trending Technologies
            </Typography>
            {(trendingTech || []).map((tech, index) => (
              <Box 
                key={tech.name} 
                sx={{ 
                  display: 'flex', 
                  alignItems: 'center', 
                  justifyContent: 'space-between', 
                  py: 1.5,
                  borderBottom: index < (trendingTech || []).length - 1 ? '1px solid #e2e8f0' : 'none'
                }}
              >
                <Box display="flex" alignItems="center" gap={1}>
                  <Box sx={{ 
                    width: 8, 
                    height: 8, 
                    borderRadius: '50%', 
                    background: tech.fill || COLORS[index % COLORS.length] 
                  }} />
                  <Typography variant="body2" sx={{ fontWeight: 500 }}>{tech.name}</Typography>
                </Box>
                <Chip 
                  label={tech.value} 
                  size="small" 
                  sx={{ bgcolor: '#6366f1', color: 'white', height: 20, fontSize: '10px' }} 
                />
              </Box>
            ))}
            {(!trendingTech || trendingTech.length === 0) && (
              <Typography variant="body2" color="text.secondary" sx={{ textAlign: 'center', py: 3 }}>
                No technology data available
              </Typography>
            )}
          </Card>
        </Grid>
      </Grid>
    </motion.div>
  );
};

export default TechnologyTrends;
