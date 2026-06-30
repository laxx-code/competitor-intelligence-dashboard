import React, { useState } from 'react';
import {
  Box, Paper, Typography, TextField, Button, Chip,
  Grid, Card, CardContent, LinearProgress,
  Alert, CircularProgress, Divider, Avatar, Container,
  Table, TableBody, TableCell, TableContainer, TableHead, TableRow,
  IconButton, Tooltip, Badge, Fade, Grow, Zoom, Slide,
  useTheme, alpha, Collapse
} from '@mui/material';
import {
  Compare as CompareIcon,
  TrendingUp as TrendingUpIcon,
  CheckCircle as CheckCircleIcon,
  Cancel as CancelIcon,
  Warning as WarningIcon,
  Star as StarIcon,
  Whatshot as WhatshotIcon,
  Business as BusinessIcon,
  Code as CodeIcon,
  People as PeopleIcon,
  Settings as SettingsIcon,
  Assessment as AssessmentIcon,
  Download as DownloadIcon,
  Share as ShareIcon,
  Psychology as PsychologyIcon,
  CloudQueue as CloudQueueIcon,
  Security as SecurityIcon,
  Speed as SpeedIcon,
  AutoAwesome as AutoAwesomeIcon,
  Insights as InsightsIcon,
  ThumbUpAlt as ThumbUpAltIcon,
  TrendingDown as TrendingDownIcon,
  Lightbulb as LightbulbIcon,
  ExpandMore as ExpandMoreIcon,
  ExpandLess as ExpandLessIcon,
  PlayArrow as PlayArrowIcon
} from '@mui/icons-material';
import axios from 'axios';

const Comparison = () => {
  const theme = useTheme();
  const [targetUrl, setTargetUrl] = useState('');
  const [competitorUrls, setCompetitorUrls] = useState('');
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState(null);
  const [error, setError] = useState(null);
  const [activeTab, setActiveTab] = useState('overview');
  const [expandedServices, setExpandedServices] = useState({});

  const handleCompare = async () => {
    if (!targetUrl.trim()) {
      setError('Please enter your company URL');
      return;
    }

    if (!competitorUrls.trim()) {
      setError('Please enter at least one competitor URL');
      return;
    }

    setLoading(true);
    setError(null);

    try {
      const urlList = competitorUrls.split('\n').filter(u => u.trim());
      const response = await axios.post('http://localhost:8000/api/compare', {
        target_url: targetUrl.trim(),
        competitor_urls: urlList
      });

      if (response.data.error) {
        setError(response.data.error);
      } else {
        setResult(response.data);
      }
    } catch (err) {
      setError(err.response?.data?.detail || 'Failed to compare companies');
    }

    setLoading(false);
  };

  const toggleServiceExpand = (category) => {
    setExpandedServices(prev => ({
      ...prev,
      [category]: !prev[category]
    }));
  };

  const getScoreColor = (score) => {
    if (score >= 80) return '#22c55e';
    if (score >= 60) return '#f59e0b';
    return '#ef4444';
  };

  const getScoreGradient = (score) => {
    if (score >= 80) return 'linear-gradient(135deg, #22c55e, #16a34a)';
    if (score >= 60) return 'linear-gradient(135deg, #f59e0b, #d97706)';
    return 'linear-gradient(135deg, #ef4444, #dc2626)';
  };

  if (loading) {
    return (
      <Box sx={{ 
        p: 4, 
        textAlign: 'center',
        minHeight: '60vh',
        display: 'flex',
        flexDirection: 'column',
        justifyContent: 'center',
        alignItems: 'center'
      }}>
        <Box sx={{ position: 'relative', display: 'inline-flex' }}>
          <CircularProgress 
            size={80} 
            sx={{ 
              color: '#6366f1',
              '& .MuiCircularProgress-circle': {
                strokeLinecap: 'round',
              }
            }} 
          />
          <Box
            sx={{
              position: 'absolute',
              top: 0,
              left: 0,
              bottom: 0,
              right: 0,
              display: 'flex',
              alignItems: 'center',
              justifyContent: 'center',
            }}
          >
            <AutoAwesomeIcon sx={{ color: '#6366f1', fontSize: 32 }} />
          </Box>
        </Box>
        <Typography variant="h5" sx={{ mt: 4, fontWeight: 700, color: '#0f172a' }}>
          Analyzing Competitive Landscape
        </Typography>
        <Typography variant="body1" color="text.secondary" sx={{ mt: 1, maxWidth: 400 }}>
          Scanning technologies, services, and market positioning of your competitors
        </Typography>
        <LinearProgress 
          sx={{ 
            mt: 4, 
            maxWidth: 400, 
            mx: 'auto',
            width: '100%',
            height: 8,
            borderRadius: 4,
            bgcolor: '#e2e8f0',
            '& .MuiLinearProgress-bar': {
              borderRadius: 4,
              background: 'linear-gradient(90deg, #6366f1, #8b5cf6)'
            }
          }} 
        />
        <Box sx={{ display: 'flex', gap: 2, mt: 3, flexWrap: 'wrap', justifyContent: 'center' }}>
          {['Scanning websites', 'Extracting services', 'Analyzing technologies', 'Generating insights'].map((step, i) => (
            <Chip 
              key={i}
              label={step}
              icon={<CircularProgress size={14} sx={{ color: '#6366f1' }} />}
              sx={{ 
                bgcolor: alpha('#6366f1', 0.08),
                color: '#6366f1',
                fontWeight: 500,
                border: '1px solid',
                borderColor: alpha('#6366f1', 0.2)
              }}
            />
          ))}
        </Box>
      </Box>
    );
  }

  return (
    <Container maxWidth="xl" sx={{ py: 4 }}>
      {/* Header Section */}
      <Paper
        elevation={0}
        sx={{ 
          p: { xs: 3, md: 4 }, 
          mb: 4, 
          borderRadius: 4,
          background: 'linear-gradient(135deg, #f8fafc 0%, #eef2ff 100%)',
          border: '1px solid #e2e8f0',
          position: 'relative',
          overflow: 'hidden'
        }}
      >
        <Box sx={{ position: 'absolute', top: -50, right: -50, opacity: 0.05 }}>
          <AssessmentIcon sx={{ fontSize: 200, color: '#6366f1' }} />
        </Box>
        <Grid container alignItems="center" justifyContent="space-between">
          <Grid item>
            <Box display="flex" alignItems="center" gap={1.5}>
              <Avatar 
                sx={{ 
                  bgcolor: '#6366f1', 
                  width: 56, 
                  height: 56,
                  boxShadow: '0 8px 24px rgba(99,102,241,0.3)'
                }}
              >
                <CompareIcon sx={{ fontSize: 32 }} />
              </Avatar>
              <Box>
                <Typography variant="h4" sx={{ fontWeight: 800, color: '#0f172a' }}>
                  Competitive Intelligence
                </Typography>
                <Typography variant="body2" color="text.secondary" sx={{ mt: 0.5 }}>
                  Compare your company against competitors to identify opportunities and gaps
                </Typography>
              </Box>
            </Box>
          </Grid>
          <Grid item>
            <Box display="flex" gap={1}>
              <Chip 
                label="Live Analysis" 
                size="medium"
                icon={<AutoAwesomeIcon sx={{ fontSize: 16 }} />}
                sx={{ 
                  bgcolor: '#dcfce7', 
                  color: '#16a34a', 
                  fontWeight: 600,
                  '& .MuiChip-icon': { color: '#16a34a' }
                }}
              />
   
            </Box>
          </Grid>
        </Grid>
      </Paper>

      {/* Input Section */}
      <Paper
        elevation={0}
        sx={{ 
          p: { xs: 3, md: 4 }, 
          mb: 4, 
          borderRadius: 4,
          border: '1px solid #e2e8f0',
          bgcolor: 'white',
          boxShadow: '0 4px 16px rgba(0,0,0,0.02)'
        }}
      >
        <Box display="flex" alignItems="center" gap={1} sx={{ mb: 3 }}>
          <SettingsIcon sx={{ color: '#6366f1' }} />
          <Typography variant="subtitle1" sx={{ fontWeight: 700, color: '#0f172a' }}>
            Configure Comparison
          </Typography>
        
        </Box>
        
        <Grid container spacing={3} alignItems="center">
          <Grid item xs={12} md={5}>
            <TextField
              fullWidth
              label="Your Company URL"
              placeholder="https://www.yourcompany.com"
              value={targetUrl}
              onChange={(e) => setTargetUrl(e.target.value)}
              sx={{
                '& .MuiOutlinedInput-root': {
                  borderRadius: 3,
                  bgcolor: '#f8fafc',
                  transition: 'all 0.2s',
                  '&:hover': { 
                    bgcolor: '#f1f5f9',
                    '& fieldset': { borderColor: '#6366f1' }
                  },
                  '&.Mui-focused': {
                    bgcolor: 'white',
                    '& fieldset': { borderColor: '#6366f1', borderWidth: 2 }
                  }
                }
              }}
              InputProps={{
                startAdornment: <BusinessIcon sx={{ color: '#6366f1', mr: 1 }} />
              }}
            />
          </Grid>
          <Grid item xs={12} md={5}>
            <TextField
              fullWidth
              multiline
              rows={3}
              label="Competitor URLs"
              placeholder="https://competitor1.com&#10;https://competitor2.com&#10;https://competitor3.com"
              value={competitorUrls}
              onChange={(e) => setCompetitorUrls(e.target.value)}
              sx={{
                '& .MuiOutlinedInput-root': {
                  borderRadius: 3,
                  bgcolor: '#f8fafc',
                  transition: 'all 0.2s',
                  '&:hover': { 
                    bgcolor: '#f1f5f9',
                    '& fieldset': { borderColor: '#6366f1' }
                  },
                  '&.Mui-focused': {
                    bgcolor: 'white',
                    '& fieldset': { borderColor: '#6366f1', borderWidth: 2 }
                  }
                }
              }}
              InputProps={{
                startAdornment: <PeopleIcon sx={{ color: '#6366f1', mr: 1, mt: 1 }} />
              }}
            />
          </Grid>
          <Grid item xs={12} md={2}>
            <Button
              fullWidth
              variant="contained"
              onClick={handleCompare}
              disabled={loading}
              sx={{
                height: 48,
                borderRadius: 3,
                background: 'linear-gradient(135deg, #6366f1 0%, #8b5cf6 100%)',
                boxShadow: '0 4px 16px rgba(99,102,241,0.3)',
                '&:hover': {
                  boxShadow: '0 6px 24px rgba(99,102,241,0.4)',
                  transform: 'translateY(-1px)',
                  background: 'linear-gradient(135deg, #4f46e5 0%, #7c3aed 100%)'
                },
                transition: 'all 0.3s ease',
                px: 2
              }}
            >
              <Box sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
                <PlayArrowIcon sx={{ fontSize: 20 }} />
                <Typography variant="body2" sx={{ fontWeight: 700, letterSpacing: 0.5 }}>
                  Run Analysis
                </Typography>
              </Box>
            </Button>
          </Grid>
        </Grid>

        {error && (
          <Fade in={!!error}>
            <Alert 
              severity="error" 
              sx={{ 
                mt: 3, 
                borderRadius: 3,
                '& .MuiAlert-icon': { fontSize: 24 }
              }}
            >
              {error}
            </Alert>
          </Fade>
        )}
      </Paper>

      {/* Results Section */}
      {result && (
        <Box>
          {/* Executive Summary */}
          <Paper
            elevation={0}
            sx={{ 
              p: { xs: 3, md: 4 }, 
              mb: 4, 
              borderRadius: 4,
              border: '1px solid #e2e8f0',
              bgcolor: 'white',
              background: 'linear-gradient(135deg, #ffffff 0%, #fafbff 100%)'
            }}
          >
            <Grid container alignItems="center" justifyContent="space-between" spacing={2}>
              <Grid item xs={12} md={8}>
                <Box display="flex" alignItems="center" gap={2}>
                  <Avatar 
                    sx={{ 
                      bgcolor: '#eef2ff', 
                      color: '#6366f1',
                      width: 64,
                      height: 64,
                      border: '2px solid #c7d2fe'
                    }}
                  >
                    <BusinessIcon sx={{ fontSize: 32 }} />
                  </Avatar>
                  <Box>
                    <Typography variant="caption" color="text.secondary" sx={{ fontWeight: 600, letterSpacing: 1 }}>
                      TARGET COMPANY
                    </Typography>
                    <Typography variant="h4" sx={{ fontWeight: 800, color: '#0f172a', mt: 0.5 }}>
                      {result.target?.company || 'Your Company'}
                    </Typography>
                    <Typography variant="body2" color="text.secondary" sx={{ display: 'flex', alignItems: 'center', gap: 0.5 }}>
                      <Box component="span" sx={{ color: '#6366f1' }}>🔗</Box>
                      {result.target?.url}
                    </Typography>
                  </Box>
                </Box>
              </Grid>
              <Grid item xs={12} md={4}>
                <Box display="flex" gap={1} justifyContent={{ xs: 'flex-start', md: 'flex-end' }}>
                  <Tooltip title="Download Report">
                    <IconButton sx={{ bgcolor: '#f1f5f9', '&:hover': { bgcolor: '#e2e8f0' } }}>
                      <DownloadIcon />
                    </IconButton>
                  </Tooltip>
                  <Tooltip title="Share Results">
                    <IconButton sx={{ bgcolor: '#f1f5f9', '&:hover': { bgcolor: '#e2e8f0' } }}>
                      <ShareIcon />
                    </IconButton>
                  </Tooltip>
                </Box>
              </Grid>
            </Grid>
          </Paper>

          {/* KPI Cards */}
          <Grid container spacing={3} sx={{ mb: 4 }}>
            {[
              {
                title: 'Shared Services',
                value: result.comparison?.service_comparison?.common_services?.length || 0,
                icon: <SettingsIcon />,
                color: '#6366f1',
                bg: '#eef2ff',
                trend: 'Common ground'
              },
              {
                title: 'Your Unique Services',
                value: result.comparison?.service_comparison?.unique_to_target?.length || 0,
                icon: <StarIcon />,
                color: '#22c55e',
                bg: '#f0fdf4',
                trend: 'Competitive advantage'
              },
              {
                title: 'Missing Services',
                value: result.comparison?.service_comparison?.missing_from_target?.length || 0,
                icon: <WarningIcon />,
                color: '#ef4444',
                bg: '#fef2f2',
                trend: 'Growth opportunity'
              },
              {
                title: 'Competitors Analyzed',
                value: result.competitors?.length || 0,
                icon: <PeopleIcon />,
                color: '#8b5cf6',
                bg: '#f5f3ff',
                trend: 'Market intelligence'
              }
            ].map((kpi, idx) => (
              <Grid item xs={12} sm={6} md={3} key={idx}>
                <Card 
                  sx={{ 
                    p: 3, 
                    borderRadius: 4,
                    border: '1px solid #e2e8f0',
                    boxShadow: '0 2px 8px rgba(0,0,0,0.02)',
                    transition: 'all 0.3s ease',
                    '&:hover': {
                      boxShadow: '0 12px 40px rgba(0,0,0,0.06)',
                      transform: 'translateY(-6px)',
                      borderColor: kpi.color
                    }
                  }}
                >
                  <Box display="flex" alignItems="center" gap={2}>
                    <Avatar sx={{ bgcolor: kpi.bg, color: kpi.color, width: 52, height: 52 }}>
                      {kpi.icon}
                    </Avatar>
                    <Box>
                      <Typography variant="caption" color="text.secondary" sx={{ fontWeight: 500, textTransform: 'uppercase', letterSpacing: 0.5 }}>
                        {kpi.title}
                      </Typography>
                      <Typography variant="h3" sx={{ fontWeight: 800, color: '#0f172a', lineHeight: 1.2 }}>
                        {kpi.value}
                      </Typography>
                      <Typography variant="caption" color="text.secondary" sx={{ display: 'flex', alignItems: 'center', gap: 0.5, mt: 0.5 }}>
                        <Box component="span" sx={{ color: kpi.color }}>•</Box>
                        {kpi.trend}
                      </Typography>
                    </Box>
                  </Box>
                </Card>
              </Grid>
            ))}
          </Grid>

          {/* Service Comparison Table */}
          <Paper
            elevation={0}
            sx={{ 
              p: { xs: 3, md: 4 }, 
              mb: 4, 
              borderRadius: 4,
              border: '1px solid #e2e8f0',
              bgcolor: 'white'
            }}
          >
            <Box display="flex" alignItems="center" justifyContent="space-between" sx={{ mb: 3 }}>
              <Typography variant="h6" sx={{ fontWeight: 700, color: '#0f172a' }}>
                <SettingsIcon sx={{ mr: 1, color: '#6366f1', verticalAlign: 'middle' }} />
                Service Analysis
              </Typography>
              <Chip 
                label={`${(result.comparison?.service_comparison?.common_services?.length || 0) + 
                        (result.comparison?.service_comparison?.unique_to_target?.length || 0) + 
                        (result.comparison?.service_comparison?.missing_from_target?.length || 0)} total services`}
                size="small"
                sx={{ bgcolor: '#f1f5f9' }}
              />
            </Box>
            
            <TableContainer>
              <Table>
                <TableHead>
                  <TableRow sx={{ bgcolor: '#f8fafc', borderRadius: 2 }}>
                    <TableCell sx={{ fontWeight: 700, color: '#0f172a' }}>Category</TableCell>
                    <TableCell sx={{ fontWeight: 700, color: '#0f172a' }}>Services</TableCell>
                    <TableCell sx={{ fontWeight: 700, color: '#0f172a' }} align="center">Count</TableCell>
                    <TableCell sx={{ fontWeight: 700, color: '#0f172a' }} align="center">Status</TableCell>
                  </TableRow>
                </TableHead>
                <TableBody>
                  {[
                    {
                      category: 'shared',
                      displayName: 'Shared Services',
                      items: result.comparison?.service_comparison?.common_services || [],
                      color: '#6366f1',
                      status: 'Common',
                      icon: <SettingsIcon sx={{ fontSize: 16 }} />
                    },
                    {
                      category: 'unique',
                      displayName: 'Your Unique Services',
                      items: result.comparison?.service_comparison?.unique_to_target || [],
                      color: '#22c55e',
                      status: 'Advantage',
                      icon: <StarIcon sx={{ fontSize: 16 }} />
                    },
                    {
                      category: 'missing',
                      displayName: 'Missing Opportunities',
                      items: result.comparison?.service_comparison?.missing_from_target || [],
                      color: '#ef4444',
                      status: 'Missing',
                      icon: <WarningIcon sx={{ fontSize: 16 }} />
                    }
                  ].map((row, idx) => {
                    const isExpanded = expandedServices[row.category] || false;
                    const displayItems = isExpanded ? row.items : row.items.slice(0, 5);
                    const hasMore = row.items.length > 5;

                    return (
                      <TableRow 
                        key={idx}
                        sx={{ 
                          '&:hover': { bgcolor: '#fafbff' },
                          transition: 'background 0.2s'
                        }}
                      >
                        <TableCell>
                          <Box display="flex" alignItems="center" gap={1}>
                            <Box sx={{ color: row.color }}>{row.icon}</Box>
                            <Typography variant="body2" sx={{ fontWeight: 600 }}>
                              {row.displayName}
                            </Typography>
                          </Box>
                        </TableCell>
                        <TableCell>
                          <Box sx={{ display: 'flex', flexWrap: 'wrap', gap: 0.5 }}>
                            {displayItems.map((item, i) => (
                              <Chip 
                                key={i} 
                                label={item} 
                                size="small" 
                                sx={{ 
                                  bgcolor: alpha(row.color, 0.08), 
                                  color: row.color,
                                  fontWeight: 500,
                                  border: '1px solid',
                                  borderColor: alpha(row.color, 0.15)
                                }} 
                              />
                            ))}
                            {hasMore && (
                              <Button
                                size="small"
                                onClick={() => toggleServiceExpand(row.category)}
                                sx={{ 
                                  minWidth: 'auto',
                                  px: 1,
                                  color: '#6366f1',
                                  fontWeight: 600,
                                  fontSize: '0.75rem',
                                  textTransform: 'none'
                                }}
                              >
                                {isExpanded ? (
                                  <><ExpandLessIcon sx={{ fontSize: 16 }} /> Show less</>
                                ) : (
                                  <><ExpandMoreIcon sx={{ fontSize: 16 }} /> +{row.items.length - 5} more</>
                                )}
                              </Button>
                            )}
                            {row.items.length === 0 && (
                              <Typography variant="body2" color="text.secondary" sx={{ fontStyle: 'italic' }}>
                                None found
                              </Typography>
                            )}
                          </Box>
                        </TableCell>
                        <TableCell align="center">
                          <Typography variant="h6" sx={{ fontWeight: 700, color: row.color }}>
                            {row.items.length}
                          </Typography>
                        </TableCell>
                        <TableCell align="center">
                          <Chip 
                            label={row.status} 
                            size="small" 
                            sx={{ 
                              bgcolor: alpha(row.color, 0.12), 
                              color: row.color,
                              fontWeight: 700,
                              minWidth: 80
                            }} 
                          />
                        </TableCell>
                      </TableRow>
                    );
                  })}
                </TableBody>
              </Table>
            </TableContainer>
          </Paper>

          {/* Technology Analysis */}
          <Paper
            elevation={0}
            sx={{ 
              p: { xs: 3, md: 4 }, 
              mb: 4, 
              borderRadius: 4,
              border: '1px solid #e2e8f0',
              bgcolor: 'white'
            }}
          >
            <Box display="flex" alignItems="center" justifyContent="space-between" sx={{ mb: 3 }}>
              <Typography variant="h6" sx={{ fontWeight: 700, color: '#0f172a' }}>
                <CodeIcon sx={{ mr: 1, color: '#8b5cf6', verticalAlign: 'middle' }} />
                Technology Stack Analysis
              </Typography>
              <Chip 
                label={`${result.comparison?.technology_comparison?.common_technologies?.length || 0} technologies`}
                size="small"
                sx={{ bgcolor: '#f1f5f9' }}
              />
            </Box>
            
            <Grid container spacing={3}>
              <Grid item xs={12} md={4}>
                <Card 
                  sx={{ 
                    p: 3, 
                    borderRadius: 3, 
                    bgcolor: '#f0fdf4',
                    border: '1px solid #bbf7d0',
                    height: '100%'
                  }}
                >
                  <Box display="flex" alignItems="center" gap={1} sx={{ mb: 2 }}>
                    <CheckCircleIcon sx={{ color: '#22c55e' }} />
                    <Typography variant="subtitle2" sx={{ fontWeight: 700, color: '#16a34a' }}>
                      Common Technologies
                    </Typography>
                    <Chip 
                      label={result.comparison?.technology_comparison?.common_technologies?.length || 0}
                      size="small"
                      sx={{ ml: 'auto', bgcolor: '#22c55e', color: 'white', fontWeight: 700 }}
                    />
                  </Box>
                  <Box sx={{ display: 'flex', flexWrap: 'wrap', gap: 0.5 }}>
                    {(result.comparison?.technology_comparison?.common_technologies || []).slice(0, 10).map((t, i) => (
                      <Chip 
                        key={i} 
                        label={t} 
                        size="small" 
                        sx={{ 
                          bgcolor: 'white',
                          border: '1px solid #bbf7d0',
                          fontWeight: 500
                        }} 
                      />
                    ))}
                  </Box>
                  <Typography variant="caption" color="text.secondary" sx={{ display: 'block', mt: 2 }}>
                    Technologies shared with competitors
                  </Typography>
                </Card>
              </Grid>
              <Grid item xs={12} md={4}>
                <Card 
                  sx={{ 
                    p: 3, 
                    borderRadius: 3, 
                    bgcolor: '#fef2f2',
                    border: '1px solid #fecaca',
                    height: '100%'
                  }}
                >
                  <Box display="flex" alignItems="center" gap={1} sx={{ mb: 2 }}>
                    <WarningIcon sx={{ color: '#ef4444' }} />
                    <Typography variant="subtitle2" sx={{ fontWeight: 700, color: '#dc2626' }}>
                      Missing Technologies
                    </Typography>
                    <Chip 
                      label={result.comparison?.technology_comparison?.missing_from_target?.length || 0}
                      size="small"
                      sx={{ ml: 'auto', bgcolor: '#ef4444', color: 'white', fontWeight: 700 }}
                    />
                  </Box>
                  <Box sx={{ display: 'flex', flexWrap: 'wrap', gap: 0.5 }}>
                    {(result.comparison?.technology_comparison?.missing_from_target || []).slice(0, 10).map((t, i) => (
                      <Chip 
                        key={i} 
                        label={t} 
                        size="small" 
                        variant="outlined"
                        sx={{ 
                          borderColor: '#fca5a5',
                          color: '#dc2626',
                          fontWeight: 500
                        }} 
                      />
                    ))}
                  </Box>
                  <Typography variant="caption" color="text.secondary" sx={{ display: 'block', mt: 2 }}>
                    Technologies to consider adopting
                  </Typography>
                </Card>
              </Grid>
              <Grid item xs={12} md={4}>
                <Card 
                  sx={{ 
                    p: 3, 
                    borderRadius: 3, 
                    bgcolor: '#eff6ff',
                    border: '1px solid #bfdbfe',
                    height: '100%'
                  }}
                >
                  <Box display="flex" alignItems="center" gap={1} sx={{ mb: 2 }}>
                    <StarIcon sx={{ color: '#2563eb' }} />
                    <Typography variant="subtitle2" sx={{ fontWeight: 700, color: '#2563eb' }}>
                      Your Unique Technologies
                    </Typography>
                    <Chip 
                      label={result.comparison?.technology_comparison?.unique_to_target?.length || 0}
                      size="small"
                      sx={{ ml: 'auto', bgcolor: '#2563eb', color: 'white', fontWeight: 700 }}
                    />
                  </Box>
                  <Box sx={{ display: 'flex', flexWrap: 'wrap', gap: 0.5 }}>
                    {(result.comparison?.technology_comparison?.unique_to_target || []).slice(0, 10).map((t, i) => (
                      <Chip 
                        key={i} 
                        label={t} 
                        size="small" 
                        sx={{ 
                          bgcolor: '#dbeafe',
                          color: '#1e40af',
                          fontWeight: 500,
                          border: '1px solid #93c5fd'
                        }} 
                      />
                    ))}
                  </Box>
                  <Typography variant="caption" color="text.secondary" sx={{ display: 'block', mt: 2 }}>
                    Technologies exclusive to your stack
                  </Typography>
                </Card>
              </Grid>
            </Grid>
          </Paper>

          {/* Strategic Recommendations - Simplified without priority labels */}
          {result.comparison?.recommendations && result.comparison.recommendations.length > 0 && (
            <Paper
              elevation={0}
              sx={{ 
                p: { xs: 3, md: 4 }, 
                mb: 4, 
                borderRadius: 4,
                border: '1px solid #e2e8f0',
                bgcolor: 'white'
              }}
            >
              <Box display="flex" alignItems="center" gap={1} sx={{ mb: 3 }}>
                <LightbulbIcon sx={{ color: '#f59e0b' }} />
                <Typography variant="h6" sx={{ fontWeight: 700, color: '#0f172a' }}>
                  Strategic Recommendations
                </Typography>
                <Chip 
                  label={`${result.comparison.recommendations.length} insights`}
                  size="small"
                  sx={{ ml: 'auto', bgcolor: '#fef3c7', color: '#d97706' }}
                />
              </Box>

              <Grid container spacing={3}>
                {result.comparison.recommendations.map((rec, idx) => (
                  <Grid item xs={12} md={6} key={idx}>
                    <Card 
                      sx={{ 
                        p: 3, 
                        borderRadius: 4,
                        border: '1px solid #e2e8f0',
                        bgcolor: '#fafbff',
                        transition: 'all 0.3s ease',
                        '&:hover': {
                          boxShadow: '0 8px 32px rgba(0,0,0,0.06)',
                          transform: 'translateY(-4px)',
                          borderColor: '#6366f1'
                        }
                      }}
                    >
                      <Box display="flex" alignItems="flex-start" gap={1.5}>
                        <Avatar 
                          sx={{ 
                            width: 40, 
                            height: 40,
                            bgcolor: '#eef2ff',
                            color: '#6366f1'
                          }}
                        >
                          <InsightsIcon />
                        </Avatar>
                        <Box flex={1}>
                          <Typography variant="subtitle1" sx={{ fontWeight: 700, color: '#0f172a' }}>
                            {rec.title}
                          </Typography>
                          
                          <Typography variant="body2" sx={{ mt: 1.5, color: '#475569', lineHeight: 1.6 }}>
                            {rec.description}
                          </Typography>
                          
                          {rec.missing && rec.missing.length > 0 && (
                            <Box sx={{ mt: 2 }}>
                              <Typography variant="caption" sx={{ fontWeight: 600, color: '#64748b' }}>
                                Related missing services:
                              </Typography>
                              <Box sx={{ display: 'flex', flexWrap: 'wrap', gap: 0.5, mt: 0.5 }}>
                                {rec.missing.slice(0, 5).map((item, i) => (
                                  <Chip key={i} label={item} size="small" variant="outlined" />
                                ))}
                              </Box>
                            </Box>
                          )}
                          
                          <Divider sx={{ my: 2 }} />
                          <Box display="flex" alignItems="center" gap={1}>
                            <AutoAwesomeIcon sx={{ fontSize: 16, color: '#6366f1' }} />
                            <Typography variant="caption" color="text.secondary">
                              {rec.reason}
                            </Typography>
                          </Box>
                        </Box>
                      </Box>
                    </Card>
                  </Grid>
                ))}
              </Grid>
            </Paper>
          )}

          {/* Footer Action Bar */}
          <Paper
            elevation={0}
            sx={{ 
              p: 3, 
              borderRadius: 4,
              border: '1px solid #e2e8f0',
              bgcolor: 'white',
              textAlign: 'center'
            }}
          >
            <Box display="flex" justifyContent="center" gap={2} flexWrap="wrap">
              <Button 
                variant="outlined" 
                startIcon={<DownloadIcon />}
                sx={{ 
                  borderRadius: 3,
                  borderColor: '#e2e8f0',
                  color: '#0f172a',
                  '&:hover': { borderColor: '#6366f1', color: '#6366f1' }
                }}
              >
                Download Report
              </Button>
              <Button 
                variant="contained" 
                startIcon={<ShareIcon />}
                sx={{ 
                  borderRadius: 3,
                  background: 'linear-gradient(135deg, #6366f1, #8b5cf6)',
                  '&:hover': {
                    background: 'linear-gradient(135deg, #4f46e5, #7c3aed)',
                    boxShadow: '0 8px 24px rgba(99,102,241,0.4)'
                  }
                }}
              >
                Share Results
              </Button>
            </Box>
          </Paper>
        </Box>
      )}
    </Container>
  );
};

export default Comparison;