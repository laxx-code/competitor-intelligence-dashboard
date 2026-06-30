import React, { useState } from 'react';
import {
  Box, Typography, TextField, Button, Chip, Paper,
  Table, TableBody, TableCell, TableContainer, TableHead, TableRow,
  Checkbox, CircularProgress, Alert, Grid
} from '@mui/material';
import { motion } from 'framer-motion';
import axios from 'axios';
import { Search, Business, LocationOn } from '@mui/icons-material';

const API_URL = 'http://localhost:8000/api';

const CompanyDiscovery = ({ onUrlsSelect }) => {
  const [location, setLocation] = useState('');
  const [companyType, setCompanyType] = useState('');
  const [loading, setLoading] = useState(false);
  const [companies, setCompanies] = useState([]);
  const [selectedUrls, setSelectedUrls] = useState([]);
  const [error, setError] = useState(null);
  const [message, setMessage] = useState('');

  const handleDiscover = async () => {
    if (!location.trim() || !companyType.trim()) {
      setError('Please enter both location and company type');
      return;
    }

    setLoading(true);
    setError(null);
    setMessage('');
    setCompanies([]);
    setSelectedUrls([]);

    try {
      // Use the correct endpoint - v2
      const response = await axios.post(`${API_URL}/discover-companies-v2`, {
        location: location.trim(),
        company_type: companyType.trim()
      });

      console.log('API Response:', response.data);

      if (response.data.error) {
        setError(response.data.error);
      } else {
        const companyList = response.data.companies || [];
        setCompanies(companyList);
        setMessage(`Found ${companyList.length} companies`);
        
        if (companyList.length === 0) {
          setError('No companies found. Try different search terms.');
        }
      }
    } catch (err) {
      console.error('Error:', err);
      setError(err.response?.data?.error || 'Failed to discover companies');
    }

    setLoading(false);
  };

  const handleSelectAll = () => {
    if (selectedUrls.length === companies.length) {
      setSelectedUrls([]);
    } else {
      setSelectedUrls(companies.map(c => c.website));
    }
  };

  const handleSelectCompany = (website) => {
    setSelectedUrls(prev =>
      prev.includes(website)
        ? prev.filter(w => w !== website)
        : [...prev, website]
    );
  };

  const handleAnalyzeSelected = () => {
    if (selectedUrls.length === 0) {
      setError('Please select at least one company');
      return;
    }
    if (onUrlsSelect) {
      onUrlsSelect(selectedUrls.join('\n'));
    }
    setSelectedUrls([]);
  };

  const popularTypes = ['Software Development', 'Digital Marketing', 'AI Development', 'Web Development', 'Mobile App Development'];
  const popularLocations = ['Pune', 'Bangalore', 'Mumbai', 'Delhi', 'Hyderabad', 'Chennai', 'Baner, Pune'];

  return (
    <Paper sx={{ p: 3, mb: 3, borderRadius: 3, border: '1px solid #e2e8f0' }}>
      <Typography variant="h6" sx={{ fontWeight: 600, mb: 2 }}>
        <Search sx={{ mr: 1, color: '#6366f1', verticalAlign: 'middle' }} />
        Company Discovery
      </Typography>

      <Grid container spacing={2}>
        <Grid item xs={12} md={5}>
          <TextField
            fullWidth
            label="Location"
            placeholder="e.g., Pune, Baner, Pune"
            value={location}
            onChange={(e) => setLocation(e.target.value)}
            InputProps={{
              startAdornment: <LocationOn sx={{ color: '#6366f1', mr: 1 }} />
            }}
          />
        </Grid>
        <Grid item xs={12} md={5}>
          <TextField
            fullWidth
            label="Company Type"
            placeholder="e.g., AI Development, Software Development"
            value={companyType}
            onChange={(e) => setCompanyType(e.target.value)}
            InputProps={{
              startAdornment: <Business sx={{ color: '#6366f1', mr: 1 }} />
            }}
          />
        </Grid>
        <Grid item xs={12} md={2}>
          <Button
            fullWidth
            variant="contained"
            onClick={handleDiscover}
            disabled={loading}
            sx={{
              height: '56px',
              background: 'linear-gradient(135deg, #0c0d3d 0%, #230d57 100%)',
              '&:hover': {
                boxShadow: '0 8px 24px rgba(99,102,241,0.4)',
                transform: 'translateY(-2px)'
              }
            }}
          >
            {loading ? <CircularProgress size={24} color="inherit" /> : 'Discover'}
          </Button>
        </Grid>
      </Grid>

      {/* Quick filters */}
      <Box sx={{ mt: 2, display: 'flex', flexWrap: 'wrap', gap: 1 }}>
        <Typography variant="caption" color="text.secondary" sx={{ mr: 1 }}>
          Popular:
        </Typography>
        {popularTypes.map((type) => (
          <Chip
            key={type}
            label={type}
            size="small"
            onClick={() => setCompanyType(type)}
            sx={{ cursor: 'pointer' }}
          />
        ))}
        {popularLocations.map((loc) => (
          <Chip
            key={loc}
            label={loc}
            size="small"
            onClick={() => setLocation(loc)}
            sx={{ cursor: 'pointer' }}
          />
        ))}
      </Box>

      {error && (
        <Alert severity={error.includes('found') ? 'info' : 'error'} sx={{ mt: 2 }}>
          {error}
        </Alert>
      )}

      {message && !error && (
        <Alert severity="info" sx={{ mt: 2 }}>
          {message}
        </Alert>
      )}

      {companies.length > 0 && (
        <Box sx={{ mt: 3}}>
          <Box display="flex" justifyContent="space-between" alignItems="center" mb={2}>
            <Typography variant="subtitle2">
              Found {companies.length} companies
            </Typography>
            <Box display="flex" gap={1}>
              <Button size="small" onClick={handleSelectAll}>
                {selectedUrls.length === companies.length ? 'Deselect All' : 'Select All'}
              </Button>
              <Button
                variant="contained"
                size="small"
                onClick={handleAnalyzeSelected}
                disabled={selectedUrls.length === 0}
                sx={{
                  color: 'white',
                  background: 'linear-gradient(135deg, #151549 0%, #13092b 100%)',
                  '&:hover': {
                    boxShadow: '0 8px 24px rgba(99,102,241,0.4)'
                  },
                  "&.Mui-disabled": {
                    color: "#fff",
                    background: "linear-gradient(135deg, #101027 0%, #10042b 100%)",
                    opacity: 0.5,
                  }
                }}
              >
                Analyze Selected ({selectedUrls.length})
              </Button>
            </Box>
          </Box>

          <TableContainer component={Paper} sx={{ borderRadius: '10px', border: '1px solid #e2e8f0' }}>
            <Table size="small">
              <TableHead sx={{ background: '#f8fafc' }}>
                <TableRow>
                  <TableCell padding="checkbox">
                    <Checkbox
                      checked={selectedUrls.length === companies.length}
                      indeterminate={selectedUrls.length > 0 && selectedUrls.length < companies.length}
                      onChange={handleSelectAll}
                    />
                  </TableCell>
                  <TableCell sx={{ fontWeight: 600 }}>#</TableCell>
                  <TableCell sx={{ fontWeight: 600 }}>Company Name</TableCell>
                  <TableCell sx={{ fontWeight: 600 }}>Website</TableCell>
                  <TableCell sx={{ fontWeight: 600 }}>Location</TableCell>
                  <TableCell sx={{ fontWeight: 600 }}>Services</TableCell>
                  <TableCell sx={{ fontWeight: 600 }}>Score</TableCell>
                </TableRow>
              </TableHead>
              <TableBody>
                {companies.map((company, index) => (
                  <motion.tr
                    key={company.website || index}
                    initial={{ opacity: 0, y: 10 }}
                    animate={{ opacity: 1, y: 0 }}
                    transition={{ delay: index * 0.02 }}
                  >
                    <TableCell padding="checkbox">
                      <Checkbox
                        checked={selectedUrls.includes(company.website)}
                        onChange={() => handleSelectCompany(company.website)}
                      />
                    </TableCell>
                    <TableCell>{index + 1}</TableCell>
                    <TableCell sx={{ fontWeight: 500 }}>{company.name || 'Unknown'}</TableCell>
                    <TableCell>
                      <a
                        href={company.website}
                        target="_blank"
                        rel="noopener noreferrer"
                        style={{ color: '#0d0d9e', textDecoration: 'none' }}
                      >
                        {company.website}
                      </a>
                    </TableCell>
                    <TableCell>{company.location || 'N/A'}</TableCell>
                    <TableCell>
                      {company.services && company.services.length > 0 ? (
                        <Box sx={{ display: 'flex', flexWrap: 'wrap', gap: 0.5 }}>
                          {company.services.slice(0, 2).map((s, i) => (
                            <Chip key={i} label={s} size="small" sx={{ height: 20, fontSize: '10px' }} />
                          ))}
                          {company.services.length > 2 && (
                            <Chip label={`+${company.services.length - 2}`} size="small" sx={{ height: 20, fontSize: '10px' }} />
                          )}
                        </Box>
                      ) : 'N/A'}
                    </TableCell>
                    <TableCell>
                      <Chip
                        label={company.score || 0}
                        size="small"
                        sx={{ 
                          bgcolor: (company.score || 0) > 70 ? '#22c55e' : (company.score || 0) > 40 ? '#f59e0b' : '#ef4444',
                          color: 'white'
                        }}
                      />
                    </TableCell>
                  </motion.tr>
                ))}
              </TableBody>
            </Table>
          </TableContainer>
        </Box>
      )}
    </Paper>
  );
};

export default CompanyDiscovery;
