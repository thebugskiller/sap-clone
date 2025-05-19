import axios from 'axios';
import { Item, ItemFormData } from '../types';

const API_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000/api/v1';

export const api = {
    async getItems(): Promise<Item[]> {
        const response = await axios.get(`${API_URL}/items/`);
        return response.data;
    },

    async getItem(id: number): Promise<Item> {
        const response = await axios.get(`${API_URL}/items/${id}`);
        return response.data;
    },

    async createItem(data: ItemFormData): Promise<Item> {
        const formData = new FormData();
        formData.append('name', data.name);
        formData.append('description', data.description);
        if (data.file) {
            formData.append('file', data.file);
        }

        const response = await axios.post(`${API_URL}/items/`, formData, {
            headers: {
                'Content-Type': 'multipart/form-data',
            },
        });
        return response.data;
    },

    async updateItem(id: number, data: ItemFormData): Promise<Item> {
        const formData = new FormData();
        formData.append('name', data.name);
        formData.append('description', data.description);
        if (data.file) {
            formData.append('file', data.file);
        }

        const response = await axios.put(`${API_URL}/items/${id}`, formData, {
            headers: {
                'Content-Type': 'multipart/form-data',
            },
        });
        return response.data;
    },

    async deleteItem(id: number): Promise<void> {
        await axios.delete(`${API_URL}/items/${id}`);
    },
}; 