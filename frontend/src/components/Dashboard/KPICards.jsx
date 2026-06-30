import React, { useState, useEffect } from 'react';
import { Box, Grid, Card, CardContent, Typography, Avatar, Chip, LinearProgress } from '@mui/material';
import { motion } from 'framer-motion';
import {
  Business as BusinessIcon,
  Code as CodeIcon,
  Settings as SettingsIcon,
  People as PeopleIcon,
  AccountTree as AccountTreeIcon,
  Timeline as TimelineIcon,
  TrendingUp as TrendingUpIcon
} from '@mui/icons-material';

const AnimatedCounter = ({ target, duration = 1000 }) => {
  const [count, setCount] = useState(0);
  
  useEffect(() => {
    let startTime;
    const animate = (timestamp) => {
      if (!startTime) startTime = timestamp;
      const progress = Math.min((timestamp - startTime) / duration, 1);
      setCount(Math.floor(progress * target));
      if (progress < 1) {
        requestAnimationFrame(animate);
      }
    };
    requestAnimationFrame(animate);
  }, [target, duration]);
  
  return <span>{count}</span>;
};

const KpiCard = ({ title, value, icon, color, subtitle, trend }) => {
  return (
    <motion.div
      whileHover={{ y: -6, transition: { duration: 0.2 } }}
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.4 }}
    >
      <Card sx={{ 
        p: 2, 
        borderRadius: 3,
        background: `linear-gradient(135deg, ${color}15 0%, ${color}05 100%)`,
        border: `1px solid ${color}25`,
        height: '100%',
        position: 'relative',
        overflow: 'hidden',
        '&:hover': {
          boxShadow: `0 8px 32px ${color}25`
        }
      }}>
        <Box sx={{ position: 'relative', zIndex: 1 }}>
          <Box display="flex" justifyContent="space-between" alignItems="flex-start">
            <Box>
              <Typography variant="caption" color="text.secondary" sx={{ fontWeight: 500 }}>
                {title}
              </Typography>
              <Typography variant="h4" sx={{ fontWeight: 700, color: color }}>
                <AnimatedCounter target={value} />
              </Typography>
              {subtitle && (
                <Typography variant="caption" color="text.secondary" sx={{ display: 'block', mt: 0.5 }}>
                  {subtitle}
                </Typography>
              )}
            </Box>
            <Avatar sx={{ bgcolor: `${color}20`, color: color, width: 40, height: 40 }}>
              {icon}
            </Avatar>
          </Box>
          {trend && (
            <Chip
              label={trend}
              size="small"
              sx={{ 
                mt: 1, 
                bgcolor: 'rgba(34,197,94,0.1)', 
                color: '#22c55e',
                height: 20,
                fontSize: '10px'
              }}
            />
          )}
        </Box>
      </Card>
    </motion.div>
  );
};

const KPICards = ({ data }) => {
  const kpis = [
    { 
      title: 'Companies Analyzed', 
      value: data.companies || 0, 
      icon: <BusinessIcon />, 
      color: '#6366f1',
      subtitle: 'Total startups'
    },
    { 
      title: 'Technologies Identified', 
      value: data.technologies || 0, 
      icon: <CodeIcon />, 
      color: '#8b5cf6',
      subtitle: 'Unique technologies'
    },
    { 
      title: 'Services Extracted', 
      value: data.services || 0, 
      icon: <SettingsIcon />, 
      color: '#a855f7',
      subtitle: 'Total services'
    },
    { 
      title: 'Clients Found', 
      value: data.clients || 0, 
      icon: <PeopleIcon />, 
      color: '#ec4899',
      subtitle: 'Client references'
    },
    { 
      title: 'Industries Covered', 
      value: data.industries || 0, 
      icon: <AccountTreeIcon />, 
      color: '#d946ef',
      subtitle: 'Sectors analyzed'
    },
    { 
      title: 'Projects Detected', 
      value: data.projects || 0, 
      icon: <TimelineIcon />, 
      color: '#f43f5e',
      subtitle: 'Case studies'
    },
  ];

  return (
    <Grid container spacing={2} sx={{ mb: 3 }}>
      {kpis.map((kpi, index) => (
        <Grid item xs={12} sm={6} md={4} key={index}>
          <KpiCard {...kpi} />
        </Grid>
      ))}
    </Grid>
  );
};

export default KPICards;
