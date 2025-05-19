import { Item, ItemFormData } from '../types';

const API_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000/api/v1';

export const api = {
    getItems: async (): Promise<Item[]> => {
        const response = await fetch(`${API_URL}/items/`);
        if (!response.ok) {
            throw new Error('Failed to fetch items');
        }
        return response.json();
    },

    getItem: async (id: number): Promise<Item> => {
        const response = await fetch(`${API_URL}/items/${id}`);
        if (!response.ok) {
            throw new Error('Failed to fetch item');
        }
        return response.json();
    },

    createItem: async (data: ItemFormData): Promise<Item> => {
        const formData = new FormData();
        formData.append('name', data.name);
        formData.append('description', data.description);
        if (data.file) {
            formData.append('file', data.file);
        }

        const response = await fetch(`${API_URL}/items/`, {
            method: 'POST',
            body: formData,
        });
        if (!response.ok) {
            throw new Error('Failed to create item');
        }
        return response.json();
    },

    updateItem: async (id: number, data: ItemFormData): Promise<Item> => {
        const formData = new FormData();
        formData.append('name', data.name);
        formData.append('description', data.description);
        if (data.file) {
            formData.append('file', data.file);
        }

        const response = await fetch(`${API_URL}/items/${id}`, {
            method: 'PUT',
            body: formData,
        });
        if (!response.ok) {
            throw new Error('Failed to update item');
        }
        return response.json();
    },

    deleteItem: async (id: number): Promise<void> => {
        const response = await fetch(`${API_URL}/items/${id}`, {
            method: 'DELETE',
        });
        if (!response.ok) {
            throw new Error('Failed to delete item');
        }
    },
}; 