import React from 'react';
import { Box, Card, CardContent, Typography, Chip, Grid } from '@mui/material';
import { motion } from 'framer-motion';
import { Timeline as TimelineIcon } from '@mui/icons-material';

const Roadmap = ({ analysis, cleanedData }) => {
  const plans = {
    '30-Day Plan': [
      'Review competitor analysis and identify gaps',
      'Conduct technology assessment',
      'Define service differentiation strategy',
      'Start client outreach'
    ],
    '90-Day Plan': [
      'Launch new services based on gap analysis',
      'Adopt key technologies',
      'Build partnerships',
      'Expand marketing efforts'
    ],
    '6-Month Plan': [
      'Scale operations',
      'Enter new markets',
      'Develop AI capabilities',
      'Achieve market leadership'
    ]
  };

  const phaseColors = {
    '30-Day Plan': '#ef4444',
    '90-Day Plan': '#f59e0b',
    '6-Month Plan': '#22c55e'
  };

  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.5 }}
    >
      <Typography variant="h6" sx={{ fontWeight: 700, mb: 2 }}>
        <TimelineIcon sx={{ mr: 1, color: '#ec4899' }} />
        Roadmap
      </Typography>

      <Grid container spacing={2}>
        {Object.entries(plans).map(([phase, items], index) => (
          <Grid item xs={12} md={4} key={index}>
            <motion.div
              whileHover={{ y: -4, transition: { duration: 0.2 } }}
            >
              <Card sx={{ 
                p: 2, 
                borderRadius: 3, 
                height: '100%',
                borderTop: `4px solid ${phaseColors[phase]}`
              }}>
                <Typography variant="subtitle2" sx={{ fontWeight: 700, color: phaseColors[phase], mb: 1 }}>
                  {phase}
                </Typography>
                {items.map((item, idx) => (
                  <Box key={idx} sx={{ display: 'flex', alignItems: 'center', gap: 1, py: 0.5 }}>
                    <Box sx={{ 
                      width: 6, 
                      height: 6, 
                      borderRadius: '50%', 
                      bgcolor: phaseColors[phase],
                      flexShrink: 0
                    }} />
                    <Typography variant="body2" sx={{ fontSize: '13px' }}>
                      {item}
                    </Typography>
                  </Box>
                ))}
              </Card>
            </motion.div>
          </Grid>
        ))}
      </Grid>
    </motion.div>
  );
};

export default Roadmap;
