import React, { useState } from 'react';
import { Box, Card, CardContent, Typography, Chip, Grid, IconButton, Collapse } from '@mui/material';
import { motion, AnimatePresence } from 'framer-motion';
import { 
  Business as BusinessIcon, 
  Code as CodeIcon, 
  People as PeopleIcon,
  ExpandMore as ExpandMoreIcon,
  ExpandLess as ExpandLessIcon,
  Link as LinkIcon
} from '@mui/icons-material';

const CompetitorCard = ({ company }) => {
  const [expanded, setExpanded] = useState(false);
  const services = company.services || [];
  const techStack = company.tech_stack || [];
  const clients = company.clients?.names || [];
  const industry = company.industry || [];

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
        <Box display="flex" justifyContent="space-between" alignItems="flex-start">
          <Box display="flex" alignItems="center" gap={1}>
            <Box 
              sx={{ 
                width: 40, 
                height: 40, 
                borderRadius: '50%', 
                bgcolor: '#6366f1',
                display: 'flex',
                alignItems: 'center',
                justifyContent: 'center',
                color: 'white',
                fontWeight: 'bold',
                fontSize: '16px'
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
          <IconButton size="small" onClick={() => setExpanded(!expanded)}>
            {expanded ? <ExpandLessIcon /> : <ExpandMoreIcon />}
          </IconButton>
        </Box>

        <Box display="flex" gap={1} flexWrap="wrap" sx={{ mt: 1 }}>
          <Chip 
            icon={<CodeIcon sx={{ fontSize: 14 }} />}
            label={`${techStack.length} Tech`} 
            size="small" 
            variant="outlined"
          />
          <Chip 
            icon={<BusinessIcon sx={{ fontSize: 14 }} />}
            label={`${services.length} Services`} 
            size="small" 
            variant="outlined"
          />
          <Chip 
            icon={<PeopleIcon sx={{ fontSize: 14 }} />}
            label={`${clients.length} Clients`} 
            size="small" 
            variant="outlined"
          />
        </Box>

        {company.founded_year && company.founded_year !== "Unknown" && (
          <Typography variant="caption" color="text.secondary" sx={{ display: 'block', mt: 1 }}>
            Founded: {company.founded_year}
          </Typography>
        )}

        <Collapse in={expanded}>
          <Box sx={{ mt: 2, pt: 2, borderTop: '1px solid #e2e8f0' }}>
            {services.length > 0 && (
              <Box sx={{ mb: 1 }}>
                <Typography variant="caption" sx={{ fontWeight: 600, color: '#6366f1' }}>
                  Services
                </Typography>
                <Box display="flex" flexWrap="wrap" gap={0.5} sx={{ mt: 0.5 }}>
                  {services.slice(0, 5).map((s, i) => (
                    <Chip key={i} label={s} size="small" sx={{ height: 20, fontSize: '9px' }} />
                  ))}
                  {services.length > 5 && (
                    <Chip label={`+${services.length - 5}`} size="small" sx={{ height: 20, fontSize: '9px' }} />
                  )}
                </Box>
              </Box>
            )}

            {techStack.length > 0 && (
              <Box sx={{ mb: 1 }}>
                <Typography variant="caption" sx={{ fontWeight: 600, color: '#6366f1' }}>
                  Technology Stack
                </Typography>
                <Box display="flex" flexWrap="wrap" gap={0.5} sx={{ mt: 0.5 }}>
                  {techStack.slice(0, 5).map((t, i) => (
                    <Chip key={i} label={t} size="small" sx={{ height: 20, fontSize: '9px' }} />
                  ))}
                  {techStack.length > 5 && (
                    <Chip label={`+${techStack.length - 5}`} size="small" sx={{ height: 20, fontSize: '9px' }} />
                  )}
                </Box>
              </Box>
            )}

            {clients.length > 0 && (
              <Box>
                <Typography variant="caption" sx={{ fontWeight: 600, color: '#6366f1' }}>
                  Clients
                </Typography>
                <Box display="flex" flexWrap="wrap" gap={0.5} sx={{ mt: 0.5 }}>
                  {clients.slice(0, 5).map((c, i) => (
                    <Chip key={i} label={c} size="small" sx={{ height: 20, fontSize: '9px' }} />
                  ))}
                  {clients.length > 5 && (
                    <Chip label={`+${clients.length - 5}`} size="small" sx={{ height: 20, fontSize: '9px' }} />
                  )}
                </Box>
              </Box>
            )}

            {industry.length > 0 && (
              <Box sx={{ mt: 1 }}>
                <Typography variant="caption" sx={{ fontWeight: 600, color: '#6366f1' }}>
                  Industries
                </Typography>
                <Box display="flex" flexWrap="wrap" gap={0.5} sx={{ mt: 0.5 }}>
                  {industry.map((ind, i) => (
                    <Chip key={i} label={ind} size="small" sx={{ height: 20, fontSize: '9px' }} />
                  ))}
                </Box>
              </Box>
            )}
          </Box>
        </Collapse>
      </Card>
    </motion.div>
  );
};

const CompetitorDetails = ({ cleanedData }) => {
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
        <BusinessIcon sx={{ mr: 1, color: '#6366f1' }} />
        Competitor Details
      </Typography>

      <Grid container spacing={2}>
        {cleanedData.map((company, index) => (
          <Grid item xs={12} sm={6} md={4} key={index}>
            <CompetitorCard company={company} />
          </Grid>
        ))}
      </Grid>
    </motion.div>
  );
};

export default CompetitorDetails;
