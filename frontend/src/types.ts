export interface Item {
    id?: number;
    name: string;
    description: string;
    image_path: string | null;
}

export interface ItemFormData {
    name: string;
    description: string;
    file: File | null;
} 