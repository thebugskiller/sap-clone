import React, { useState, useEffect } from 'react';
import {
  Container,
  Typography,
  Box,
  Paper,
  Button,
  Dialog,
  DialogTitle,
  DialogContent,
  DialogActions,
  TextField,
  IconButton,
} from '@mui/material';
import { Add as AddIcon, Delete as DeleteIcon, Edit as EditIcon } from '@mui/icons-material';
import { Item, ItemFormData } from './types';
import { api } from './services/api';

function App() {
  const BASE_URL = process.env.REACT_APP_BASE_URL || 'http://localhost:8000';
  const [items, setItems] = useState<Item[]>([]);
  const [open, setOpen] = useState(false);
  const [editingItem, setEditingItem] = useState<Item | null>(null);
  const [formData, setFormData] = useState<ItemFormData>({
    name: '',
    description: '',
    file: null,
  });

  useEffect(() => {
    loadItems();
  }, []);

  const loadItems = async () => {
    try {
      const data = await api.getItems();
      setItems(data);
    } catch (error) {
      console.error('Error loading items:', error);
    }
  };

  const handleOpen = (item?: Item) => {
    if (item) {
      setEditingItem(item);
      setFormData({
        name: item.name,
        description: item.description,
        file: null,
      });
    } else {
      setEditingItem(null);
      setFormData({
        name: '',
        description: '',
        file: null,
      });
    }
    setOpen(true);
  };

  const handleClose = () => {
    setOpen(false);
    setEditingItem(null);
    setFormData({
      name: '',
      description: '',
      file: null,
    });
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    try {
      if (editingItem) {
        await api.updateItem(editingItem.id!, formData);
      } else {
        await api.createItem(formData);
      }
      handleClose();
      loadItems();
    } catch (error) {
      console.error('Error saving item:', error);
    }
  };

  const handleDelete = async (id: number) => {
    try {
      await api.deleteItem(id);
      loadItems();
    } catch (error) {
      console.error('Error deleting item:', error);
    }
  };

  const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    if (e.target.files && e.target.files[0]) {
      setFormData({
        ...formData,
        file: e.target.files[0],
      });
    }
  };

  return (
    <Container maxWidth="lg">
      <Box sx={{ my: 4 }}>
        <Typography variant="h4" component="h1" gutterBottom>
          CRUD System with File Upload
        </Typography>
        
        <Button
          variant="contained"
          startIcon={<AddIcon />}
          onClick={() => handleOpen()}
          sx={{ mb: 3 }}
        >
          Add New Item
        </Button>

        <Box sx={{ 
          display: 'grid', 
          gridTemplateColumns: 'repeat(auto-fill, minmax(300px, 1fr))',
          gap: 3 
        }}>
          {items.map((item) => (
            <Paper
              key={item.id}
              sx={{
                p: 2,
                display: 'flex',
                flexDirection: 'column',
                height: '100%',
              }}
            >
              {item.image_path && (
                <Box
                  component="img"
                  src={`${BASE_URL}/uploads/${item.image_path.split('/').pop()}`}
                  alt={item.name}
                  sx={{
                    width: '100%',
                    height: 200,
                    objectFit: 'cover',
                    mb: 2,
                  }}
                />
              )}
              <Typography variant="h6" component="h2">
                {item.name}
              </Typography>
              <Typography color="text.secondary" sx={{ mb: 2 }}>
                {item.description}
              </Typography>
              <Box sx={{ mt: 'auto', display: 'flex', justifyContent: 'flex-end' }}>
                <IconButton onClick={() => handleOpen(item)} color="primary">
                  <EditIcon />
                </IconButton>
                <IconButton onClick={() => handleDelete(item.id!)} color="error">
                  <DeleteIcon />
                </IconButton>
              </Box>
            </Paper>
          ))}
        </Box>

        <Dialog open={open} onClose={handleClose} maxWidth="sm" fullWidth>
          <form onSubmit={handleSubmit}>
            <DialogTitle>
              {editingItem ? 'Edit Item' : 'Add New Item'}
            </DialogTitle>
            <DialogContent>
              <TextField
                autoFocus
                margin="dense"
                label="Name"
                fullWidth
                value={formData.name}
                onChange={(e) => setFormData({ ...formData, name: e.target.value })}
                required
              />
              <TextField
                margin="dense"
                label="Description"
                fullWidth
                multiline
                rows={4}
                value={formData.description}
                onChange={(e) => setFormData({ ...formData, description: e.target.value })}
                required
              />
              <Button
                variant="outlined"
                component="label"
                fullWidth
                sx={{ mt: 2 }}
              >
                Upload Image
                <input
                  type="file"
                  hidden
                  accept="image/png,image/jpeg,image/bmp"
                  onChange={handleFileChange}
                />
              </Button>
              {formData.file && (
                <Typography variant="body2" sx={{ mt: 1 }}>
                  Selected file: {formData.file.name}
                </Typography>
              )}
            </DialogContent>
            <DialogActions>
              <Button onClick={handleClose}>Cancel</Button>
              <Button type="submit" variant="contained">
                {editingItem ? 'Update' : 'Create'}
              </Button>
            </DialogActions>
          </form>
        </Dialog>
      </Box>
    </Container>
  );
}

export default App;
