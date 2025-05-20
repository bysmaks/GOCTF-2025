import { NextApiRequest, NextApiResponse } from 'next';
import fs from 'fs';
import path from 'path';

function getFilesRecursively(dir: string, baseDir: string): string[] {
  const files: string[] = [];
  const entries = fs.readdirSync(dir, { withFileTypes: true });
  
  for (const entry of entries) {
    const fullPath = path.join(dir, entry.name);
    const relativePath = path.relative(baseDir, fullPath);
    
    if (entry.isDirectory()) {
      files.push(...getFilesRecursively(fullPath, baseDir));
    } else {
      if (!entry.name.endsWith('.symlink')) {
        files.push(relativePath);
      }
    }
  }
  
  return files;
}

export default function handler(req: NextApiRequest, res: NextApiResponse) {
  try {
    const { id } = req.query;
    
    if (!id || Array.isArray(id)) {
      return res.status(400).json({ error: 'Invalid ID' });
    }
    
    const uploadDir = path.join(process.cwd(), 'public', 'uploads', id);
    
    if (!fs.existsSync(uploadDir)) {
      return res.status(404).json({ error: 'Upload not found' });
    }
    
    const files = getFilesRecursively(uploadDir, uploadDir);
    
    return res.status(200).json({ 
      id,
      files
    });
  } catch (error) {
    const errorMessage = error instanceof Error ? error.message : String(error);
    return res.status(500).json({ error: errorMessage });
  }
} 