import React, { useState, useEffect } from 'react';
import { ThemeProvider, createTheme } from '@mui/material/styles';
import { CssBaseline, Box, Container, Typography, Paper, Grid, Card, CardContent, Chip, Button, TextField, LinearProgress, Avatar, Divider, Accordion, AccordionSummary, AccordionDetails, CircularProgress, IconButton, Badge } from '@mui/material';
import { motion, AnimatePresence } from 'framer-motion';
import { 
  BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip as RechartsTooltip, Legend, ResponsiveContainer, Cell 
} from 'recharts';
import axios from 'axios';
import CompanyDiscovery from './components/CompanyDiscovery';
import Comparison from './components/Comparison';
import Dashboard from './components/Dashboard';

// Icons
import { 
  Whatshot as WhatshotIcon, 
  Code as CodeIcon, 
  AccountTree as AccountTreeIcon, 
  SettingsApplications as SettingsIcon, 
  ExpandMore as ExpandMoreIcon, 
  DataUsage as DataUsageIcon, 
  Business as BusinessIcon,
  TrendingUp as TrendingUpIcon,
  Rocket as RocketIcon,
  Menu as MenuIcon,
  Dashboard as DashboardIcon,
  Search as SearchIcon,
  Notifications as NotificationsIcon,
  Person as PersonIcon,
  Compare as CompareIcon
} from '@mui/icons-material';

const API_URL = 'http://localhost:8000/api';

const COLORS = ['#6366f1', '#8b5cf6', '#a855f7', '#d946ef', '#ec4899', '#f43f5e', '#fb7185', '#f472b6'];

const TECH_COLORS = {
  'Python': '#3776AB', 'JavaScript': '#F7DF1E', 'React': '#61DAFB',
  'Angular': '#DD0031', 'Vue.js': '#4FC08D', 'Node.js': '#339933',
  'Django': '#092E20', 'Flask': '#000000', 'Java': '#007396',
  'AWS': '#FF9900', 'Azure': '#0078D4', 'GCP': '#4285F4',
  'Docker': '#2496ED', 'Kubernetes': '#326CE5', 'TensorFlow': '#FF6F00',
  'PyTorch': '#EE4C2C', 'MongoDB': '#47A248', 'PostgreSQL': '#336791',
  'MySQL': '#4479A1', 'Redis': '#DC382D', 'Git': '#F05032',
  'OpenAI': '#412991', 'LangChain': '#1C3C6C', 'LLM': '#7C3AED'
};

const theme = createTheme({
  palette: {
    mode: 'light',
    primary: { main: '#6366f1', light: '#818cf8', dark: '#4f46e5' },
    secondary: { main: '#8b5cf6', light: '#a78bfa', dark: '#7c3aed' },
    background: { default: '#f8fafc', paper: '#ffffff' },
    text: { primary: '#0f172a', secondary: '#475569' }
  },
  shape: { borderRadius: 12 },
  typography: {
    fontFamily: '"Inter", -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif'
  }
});

function App() {
  const [urls, setUrls] = useState('');
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState(null);
  const [reports, setReports] = useState([]);
  const [activeTab, setActiveTab] = useState('analyze');
  const [error, setError] = useState(null);
  const [backendStatus, setBackendStatus] = useState('checking');
  const [expandedCompanies, setExpandedCompanies] = useState({});
  const [expandedRawData, setExpandedRawData] = useState({});
  const [techData, setTechData] = useState([]);
  const [trendingTech, setTrendingTech] = useState([]);
  const [companyCount, setCompanyCount] = useState(0);
  const [totalTech, setTotalTech] = useState(0);

  useEffect(() => {
    checkBackend();
    loadReports();
  }, []);

  useEffect(() => {
    if (result?.results?.AnalyzerAgent?.analysis) {
      const analysis = result.results.AnalyzerAgent.analysis;
      if (analysis.technology_analysis?.top_technologies) {
        const data = analysis.technology_analysis.top_technologies.map((item) => ({
          name: item.name,
          value: item.count,
          fill: TECH_COLORS[item.name] || '#6366f1'
        }));
        setTechData(data);
        setTotalTech(analysis.technology_analysis.total_technologies || 0);
        const sorted = [...data].sort((a, b) => b.value - a.value);
        setTrendingTech(sorted.slice(0, 5));
      }
      if (analysis.total_companies) setCompanyCount(analysis.total_companies);
    }
  }, [result]);

  const checkBackend = async () => {
    try {
      await axios.get('http://localhost:8000/health');
      setBackendStatus('connected');
    } catch (e) {
      setBackendStatus('disconnected');
    }
  };

  const loadReports = async () => {
    try {
      const res = await axios.get(`${API_URL}/reports`);
      setReports(res.data.reports || []);
    } catch (e) {
      console.error(e);
    }
  };

  const handleAnalyze = async () => {
    if (!urls.trim()) {
      alert('Please enter at least one URL');
      return;
    }
    setLoading(true);
    setResult(null);
    setError(null);
    try {
      const urlList = urls.split('\n').filter(u => u.trim());
      const res = await axios.post(`${API_URL}/analyze`, { urls: urlList });
      setResult(res.data);
      await loadReports();
    } catch (e) {
      setError(e.response?.data?.detail || e.message);
      alert('Error: ' + (e.response?.data?.detail || e.message));
    }
    setLoading(false);
  };

  const toggleExpand = (name) => {
    setExpandedCompanies(prev => ({ ...prev, [name]: !prev[name] }));
  };

  const toggleRawData = (name) => {
    setExpandedRawData(prev => ({ ...prev, [name]: !prev[name] }));
  };

  const getCleanedData = () => result?.results?.CleanerAgent?.cleaned_data || [];
  const getRawData = () => result?.results?.EnhancedScraperAgent?.scraped_data || [];
  const getAnalysis = () => result?.results?.AnalyzerAgent?.analysis || null;

  const cleanedData = getCleanedData();
  const rawData = getRawData();
  const analysis = getAnalysis();

  return (
    <ThemeProvider theme={theme}>
      <CssBaseline />
      <Box sx={{ display: 'flex', minHeight: '100vh', bgcolor: '#f8fafc' }}>
        {/* Sidebar */}
        <Box
          sx={{
            width: 260,
            minWidth: 260,
            bgcolor: 'white',
            borderRight: '1px solid #e2e8f0',
            height: '100vh',
            position: 'sticky',
            top: 0,
            overflow: 'auto',
            display: { xs: 'none', md: 'block' }
          }}
        >
          <Box sx={{ p: 3 }}>
            <Box display="flex" alignItems="center" gap={1.5} mb={4}>
             
              <Typography variant="h6" sx={{ fontWeight: 700, fontSize: '16px' }}>
                Startup Intel
              </Typography>
            </Box>

            <Box display="flex" flexDirection="column" gap={0.5}>
              {['analyze', 'comparison', 'dashboard'].map((tab) => (
                <motion.button
                  key={tab}
                  whileHover={{ x: 4 }}
                  whileTap={{ scale: 0.98 }}
                  onClick={() => setActiveTab(tab)}
                  style={{
                    width: '100%',
                    padding: '10px 16px',
                    borderRadius: '10px',
                    border: 'none',
                    background: activeTab === tab ? 'linear-gradient(135deg, #6366f1, #8b5cf6)' : 'transparent',
                    color: activeTab === tab ? 'white' : '#475569',
                    fontWeight: 600,
                    fontSize: '14px',
                    cursor: 'pointer',
                    display: 'flex',
                    alignItems: 'center',
                    gap: '12px',
                    transition: 'all 0.2s ease',
                    boxShadow: activeTab === tab ? '0 4px 16px rgba(99,102,241,0.3)' : 'none'
                  }}
                >
                  {tab === 'analyze' && <SearchIcon />}
                  {tab === 'comparison' && <CompareIcon />}
                  {tab === 'dashboard' && <DashboardIcon />}
                  {tab === 'analyze' && 'Analyze'}
                  {tab === 'comparison' && 'Compare'}
                  {tab === 'dashboard' && 'Dashboard'}
                </motion.button>
              ))}
            </Box>

            
          </Box>
        </Box>

        {/* Main Content */}
        <Box sx={{ flex: 1, minWidth: 0 }}>
          {/* Top Navigation */}
          <Box
            sx={{
              bgcolor: 'white',
              borderBottom: '1px solid #e2e8f0',
              px: { xs: 2, md: 4 },
              py: 2,
              position: 'sticky',
              top: 0,
              zIndex: 1100,
              backdropFilter: 'blur(12px)',
              bgcolor: 'rgba(255,255,255,0.8)'
            }}
          >
            <Box display="flex" alignItems="center" justifyContent="space-between">
              <Box display="flex" alignItems="center" gap={2}>
                <Typography variant="h6" sx={{ fontWeight: 700, fontSize: { xs: '16px', md: '20px' } }}>
                  {activeTab === 'analyze' && ' Competitor Analysis'}
                  {activeTab === 'comparison' && ' Company Comparison'}
                  {activeTab === 'dashboard' && 'Intelligence Dashboard'}
                </Typography>
              </Box>
              <Box display="flex" alignItems="center" gap={1}>
                <Chip
                  label={backendStatus === 'connected' ? '🟢 Live' : '🔴 Offline'}
                  size="small"
                  sx={{
                    bgcolor: backendStatus === 'connected' ? 'rgba(34,197,94,0.1)' : 'rgba(239,68,68,0.1)',
                    color: backendStatus === 'connected' ? '#22c55e' : '#ef4444',
                    fontWeight: 600
                  }}
                />
                
              </Box>
            </Box>
          </Box>

          {/* Page Content */}
          <Box sx={{ p: { xs: 2, md: 4 } }}>
            <AnimatePresence mode="wait">
              {activeTab === 'analyze' && (
                <motion.div
                  key="analyze"
                  initial={{ opacity: 0, y: 10 }}
                  animate={{ opacity: 1, y: 0 }}
                  exit={{ opacity: 0, y: -10 }}
                  transition={{ duration: 0.3 }}
                >
                  <CompanyDiscovery onUrlsSelect={(urls) => setUrls(urls)} />

                  <Paper sx={{ p: 3, mb: 3, borderRadius: 3 }}>
                    <Typography variant="subtitle1" sx={{ fontWeight: 600, mb: 1 }}>
                      Enter Competitor URLs
                    </Typography>
                    <Typography variant="body2" color="text.secondary" sx={{ mb: 2 }}>
                      One URL per line — Analyze startup competitors
                    </Typography>
                    <TextField
                      fullWidth
                      multiline
                      rows={3}
                      placeholder="https://example.com\nhttps://another-startup.com"
                      value={urls}
                      onChange={(e) => setUrls(e.target.value)}
                      sx={{
                        '& .MuiOutlinedInput-root': {
                          borderRadius: '12px',
                          backgroundColor: 'rgba(255,255,255,0.7)',
                          fontFamily: 'monospace',
                          fontSize: '14px',
                          '&:hover fieldset': { borderColor: '#6366f1' },
                          '&.Mui-focused fieldset': { borderColor: '#6366f1', borderWidth: '2px' }
                        }
                      }}
                    />
                    <Box sx={{ display: 'flex', justifyContent: 'center', alignItems: 'center', mt: 3 }}>
                      <motion.button
                        whileHover={!loading ? { scale: 1.02 } : {}}
                        whileTap={!loading ? { scale: 0.98 } : {}}
                        onClick={handleAnalyze}
                        disabled={loading}
                        style={{
                          padding: '10px 36px',
                          background: loading ? '#94a3b8' : 'linear-gradient(135deg, #6366f1 0%, #8b5cf6 100%)',
                          color: 'white',
                          border: 'none',
                          borderRadius: '10px',
                          cursor: loading ? 'not-allowed' : 'pointer',
                          fontSize: '14px',
                          fontWeight: 600,
                          boxShadow: loading ? 'none' : '0 4px 16px rgba(99,102,241,0.3)',
                          opacity: loading ? 0.7 : 1,
                          transition: 'all 0.2s ease'
                        }}
                      >
                        {loading ? '⏳ Analyzing...' : 'Start Analysis'}
                      </motion.button>
                    </Box>
                  </Paper>

                  {loading && (
                    <motion.div initial={{ opacity: 0 }} animate={{ opacity: 1 }}>
                      <Paper sx={{ p: 3, borderRadius: 3, bgcolor: 'rgba(99,102,241,0.04)' }}>
                        <Typography variant="body2" sx={{ fontWeight: 500 }}>AI Agents are working...</Typography>
                        <LinearProgress sx={{ mt: 1, height: 4, borderRadius: 2 }} />
                      </Paper>
                    </motion.div>
                  )}

                  {error && (
                    <motion.div initial={{ opacity: 0, x: -20 }} animate={{ opacity: 1, x: 0 }}>
                      <Paper sx={{ p: 2, borderRadius: 3, bgcolor: '#fef2f2', border: '1px solid #fecaca' }}>
                        <Typography variant="body2" color="error"><strong> Error:</strong> {error}</Typography>
                      </Paper>
                    </motion.div>
                  )}

                  {result && (
                    <motion.div
                      initial={{ opacity: 0 }}
                      animate={{ opacity: 1 }}
                      transition={{ duration: 0.4 }}
                    >
                      <Grid container spacing={2} sx={{ mb: 3 }}>
                        {[
                          { title: 'Startups', value: analysis?.total_companies || 0, icon: <BusinessIcon />, color: '#6366f1' },
                          { title: 'Technologies', value: totalTech, icon: <CodeIcon />, color: '#8b5cf6' },
                          { title: 'Services', value: analysis?.service_analysis?.total_services || 0, icon: <SettingsIcon />, color: '#a855f7' },
                        ].map((stat, index) => (
                          <Grid item xs={12} sm={4} key={index}>
                            <motion.div
                              initial={{ opacity: 0, y: 10 }}
                              animate={{ opacity: 1, y: 0 }}
                              transition={{ delay: index * 0.05 }}
                            >
                              <Paper sx={{ p: 2, borderRadius: 3, textAlign: 'center' }}>
                                <Avatar sx={{ bgcolor: stat.color, width: 40, height: 40, mx: 'auto', mb: 1 }}>
                                  {stat.icon}
                                </Avatar>
                                <Typography variant="h5" sx={{ fontWeight: 700, color: stat.color }}>
                                  {stat.value}
                                </Typography>
                                <Typography variant="caption" color="text.secondary">
                                  {stat.title}
                                </Typography>
                              </Paper>
                            </motion.div>
                          </Grid>
                        ))}
                      </Grid>

                      <Paper sx={{ p: 3, mb: 3, borderRadius: 3 }}>
                        <Box display="flex" alignItems="center" justifyContent="space-between" mb={2}>
                          <Typography variant="h6" sx={{ fontWeight: 600 }}>
                            <DataUsageIcon sx={{ color: '#6366f1', mr: 1, verticalAlign: 'middle' }} />
                            Raw Data ({rawData.length} companies)
                          </Typography>
                          <Chip label={`${rawData.length} companies`} size="small" sx={{ bgcolor: '#6366f1', color: 'white' }} />
                        </Box>
                        <Divider sx={{ mb: 2 }} />
                        {rawData.length === 0 ? (
                          <Typography variant="body2" color="text.secondary" align="center" sx={{ py: 4 }}>
                            No raw data available. Run an analysis first!
                          </Typography>
                        ) : (
                          rawData.map((item, index) => {
                            const companyName = item.data?.company_name || `Company ${index + 1}`;
                            const isExpanded = expandedRawData[companyName] || false;
                            const data = item.data || {};
                            return (
                              <Accordion
                                key={index}
                                expanded={isExpanded}
                                onChange={() => toggleRawData(companyName)}
                                sx={{
                                  mb: 1,
                                  borderRadius: '12px !important',
                                  border: '1px solid #e2e8f0',
                                  boxShadow: 'none',
                                  '&:before': { display: 'none' }
                                }}
                              >
                                <AccordionSummary expandIcon={<ExpandMoreIcon />} sx={{ borderRadius: '12px' }}>
                                  <Box display="flex" alignItems="center" gap={2} width="100%">
                                    <Avatar sx={{ bgcolor: '#6366f1', width: 28, height: 28, fontSize: 12 }}>{index + 1}</Avatar>
                                    <Box flex={1}>
                                      <Typography variant="subtitle2" sx={{ fontWeight: 600 }}>{companyName}</Typography>
                                      <Typography variant="caption" color="text.secondary">{item.url}</Typography>
                                    </Box>
                                    <Chip
                                      label={item.status === 'success' ? 'Success' : ' Failed'}
                                      size="small"
                                      sx={{
                                        bgcolor: item.status === 'success' ? '#d4edda' : '#f8d7da',
                                        color: item.status === 'success' ? '#155724' : '#721c24'
                                      }}
                                    />
                                  </Box>
                                </AccordionSummary>
                                <AccordionDetails>
                                  {item.status === 'failed' ? (
                                    <Typography color="error" variant="caption">Error: {item.error}</Typography>
                                  ) : (
                                    <Box>
                                      <Grid container spacing={1}>
                                        <Grid item xs={12} md={6}>
                                          <Typography variant="caption" sx={{ fontWeight: 600, color: '#6366f1' }}>Basic Info</Typography>
                                          <Paper sx={{ p: 2, borderRadius: 2, bgcolor: '#f8fafc', mt: 0.5 }}>
                                            <div><strong>Name:</strong> {data.company_name || 'N/A'}</div>
                                            <div><strong>Founded:</strong> {data.founded_year || 'Unknown'}</div>
                                          </Paper>
                                        </Grid>
                                        <Grid item xs={12} md={6}>
                                          <Typography variant="caption" sx={{ fontWeight: 600, color: '#6366f1' }}>About</Typography>
                                          <Paper sx={{ p: 2, borderRadius: 2, bgcolor: '#f8fafc', mt: 0.5 }}>
                                            <div>{data.about ? data.about.substring(0, 150) + '...' : 'N/A'}</div>
                                          </Paper>
                                        </Grid>
                                      </Grid>
                                      {data.services && data.services.length > 0 && (
                                        <Box sx={{ mt: 2 }}>
                                          <Typography variant="caption" sx={{ fontWeight: 600, color: '#6366f1' }}>
                                            🛠️ Services ({data.services.length})
                                          </Typography>
                                          <Box sx={{ display: 'flex', flexWrap: 'wrap', gap: 0.5, mt: 0.5 }}>
                                            {data.services.slice(0, 5).map((service, i) => (
                                              <Chip key={i} label={service} size="small" sx={{ height: 24 }} />
                                            ))}
                                            {data.services.length > 5 && (
                                              <Chip label={`+${data.services.length - 5}`} size="small" />
                                            )}
                                          </Box>
                                        </Box>
                                      )}
                                      {data.tech_stack && data.tech_stack.length > 0 && (
                                        <Box sx={{ mt: 2 }}>
                                          <Typography variant="caption" sx={{ fontWeight: 600, color: '#6366f1' }}>
                                             Tech Stack
                                          </Typography>
                                          <Box sx={{ display: 'flex', flexWrap: 'wrap', gap: 0.5, mt: 0.5 }}>
                                            {data.tech_stack.map((tech, i) => (
                                              <Chip key={i} label={tech} size="small" sx={{ height: 24 }} />
                                            ))}
                                          </Box>
                                        </Box>
                                      )}
                                    </Box>
                                  )}
                                </AccordionDetails>
                              </Accordion>
                            );
                          })
                        )}
                      </Paper>

                      {cleanedData.length > 0 && (
                        <Box>
                          <Typography variant="h6" sx={{ fontWeight: 600, mb: 2 }}>
                            🏢 Startup Analysis
                          </Typography>
                          <Grid container spacing={2}>
                            {cleanedData.map((company, index) => {
                              const isExpanded = expandedCompanies[company.company] || false;
                              const services = company.services || [];
                              const techStack = company.tech_stack || [];
                              const clients = company.clients || {};
                              const clientNames = clients.names || [];
                              const projects = company.projects || [];
                              return (
                                <Grid item xs={12} md={6} key={index}>
                                  <Paper sx={{ p: 2, borderRadius: 3 }}>
                                    <Box display="flex" justifyContent="space-between" alignItems="center" sx={{ cursor: 'pointer' }} onClick={() => toggleExpand(company.company)}>
                                      <Box>
                                        <Typography variant="h6" sx={{ color: '#6366f1', fontWeight: 600, fontSize: '16px' }}>
                                          {company.company || 'Unknown'}
                                        </Typography>
                                        <Typography variant="caption" color="text.secondary">{company.url}</Typography>
                                      </Box>
                                      <motion.button
                                        whileHover={{ scale: 1.05 }}
                                        whileTap={{ scale: 0.95 }}
                                        style={{
                                          background: 'none',
                                          border: 'none',
                                          color: '#6366f1',
                                          cursor: 'pointer',
                                          fontSize: '13px',
                                          fontWeight: 600,
                                          padding: '4px 10px',
                                          borderRadius: '8px'
                                        }}
                                      >
                                        {isExpanded ? '▼' : '▶'}
                                      </motion.button>
                                    </Box>
                                    <Box sx={{ mt: 1, fontSize: '13px', color: '#475569' }}>
                                      {company.founded_year && company.founded_year !== "Unknown" && (
                                        <span><strong></strong> {company.founded_year} </span>
                                      )}
                                      {company.team_size && company.team_size.count && (
                                        <span><strong></strong> {company.team_size.count} </span>
                                      )}
                                    </Box>
                                    <Box sx={{ mt: 1 }}>
                                      <Typography variant="caption" sx={{ fontWeight: 600, color: '#475569' }}>🛠️ Services:</Typography>
                                      <Box sx={{ display: 'flex', flexWrap: 'wrap', gap: 0.5, mt: 0.5 }}>
                                        {services.slice(0, isExpanded ? services.length : 3).map((service, i) => {
                                          const name = typeof service === 'string' ? service : service.name;
                                          return name ? (
                                            <span
                                              key={i}
                                              style={{
                                                display: 'inline-block',
                                                padding: '3px 14px',
                                                borderRadius: '20px',
                                                margin: '2px',
                                                fontSize: '11px',
                                                fontWeight: 500,
                                                background: '#eef2ff',
                                                color: '#6366f1'
                                              }}
                                            >
                                              {name.length > 20 ? name.substring(0, 20) + '...' : name}
                                            </span>
                                          ) : null;
                                        })}
                                        {!isExpanded && services.length > 3 && (
                                          <span
                                            style={{
                                              display: 'inline-block',
                                              padding: '3px 14px',
                                              borderRadius: '20px',
                                              margin: '2px',
                                              fontSize: '11px',
                                              fontWeight: 600,
                                              background: '#e0e7ff',
                                              color: '#6366f1',
                                              cursor: 'pointer'
                                            }}
                                            onClick={(e) => { e.stopPropagation(); toggleExpand(company.company); }}
                                          >
                                            +{services.length - 3}
                                          </span>
                                        )}
                                      </Box>
                                    </Box>
                                    {isExpanded && (
                                      <motion.div
                                        initial={{ opacity: 0, height: 0 }}
                                        animate={{ opacity: 1, height: 'auto' }}
                                        transition={{ duration: 0.3 }}
                                        style={{ marginTop: '12px', fontSize: '13px', color: '#475569' }}
                                      >
                                        {techStack.length > 0 && (
                                          <Box sx={{ mb: 1 }}><strong> Tech:</strong> {techStack.join(', ')}</Box>
                                        )}
                                        {clientNames.length > 0 && (
                                          <Box sx={{ mb: 1 }}>
                                            <strong>Clients:</strong> {clientNames.slice(0, 3).join(', ')}
                                            {clientNames.length > 3 && ` +${clientNames.length - 3}`}
                                          </Box>
                                        )}
                                        {projects.length > 0 && (
                                          <Box sx={{ mb: 1 }}><strong>📋 Projects:</strong> {projects.length}</Box>
                                        )}
                                        {company.about && company.about !== "No about information available" && (
                                          <Box sx={{ mt: 1, color: '#475569', fontSize: '12px' }}>
                                            {company.about.substring(0, 200)}...
                                          </Box>
                                        )}
                                      </motion.div>
                                    )}
                                  </Paper>
                                </Grid>
                              );
                            })}
                          </Grid>
                        </Box>
                      )}
                    </motion.div>
                  )}
                </motion.div>
              )}

              {activeTab === 'comparison' && (
                <motion.div
                  key="comparison"
                  initial={{ opacity: 0, y: 10 }}
                  animate={{ opacity: 1, y: 0 }}
                  exit={{ opacity: 0, y: -10 }}
                  transition={{ duration: 0.3 }}
                >
                  <Comparison />
                </motion.div>
              )}

              {activeTab === 'dashboard' && (
                <motion.div
                  key="dashboard"
                  initial={{ opacity: 0, y: 10 }}
                  animate={{ opacity: 1, y: 0 }}
                  exit={{ opacity: 0, y: -10 }}
                  transition={{ duration: 0.3 }}
                >
                  <Dashboard 
                    analysis={analysis}
                    cleanedData={cleanedData}
                    techData={techData}
                    trendingTech={trendingTech}
                    companyCount={companyCount}
                    totalTech={totalTech}
                  />
                </motion.div>
              )}
            </AnimatePresence>
          </Box>
        </Box>
      </Box>
    </ThemeProvider>
  );
}

export default App;
