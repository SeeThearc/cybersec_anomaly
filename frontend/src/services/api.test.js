import { describe, it, expect, vi, beforeEach } from 'vitest';
import axios from 'axios';
import { getSystemStats, askCopilot } from './api';

// Mock axios completely
vi.mock('axios');

describe('Frontend API Service Tests', () => {
  beforeEach(() => {
    vi.clearAllMocks();
  });

  it('should fetch system stats successfully', async () => {
    const mockData = { total_users: 100, active_threats: 5 };
    axios.get.mockResolvedValueOnce({ data: mockData });

    const result = await getSystemStats();
    
    expect(axios.get).toHaveBeenCalledWith('http://localhost:8000/statistics');
    expect(result).toEqual(mockData);
  });

  it('should send a message to copilot and return answer', async () => {
    const mockResponse = { answer: "This is a mock answer." };
    axios.post.mockResolvedValueOnce({ data: mockResponse });

    const question = "Why was a user flagged?";
    const result = await askCopilot(question);

    expect(axios.post).toHaveBeenCalledWith('http://localhost:8000/copilot', { question });
    expect(result).toEqual(mockResponse);
  });

  it('should handle API errors gracefully', async () => {
    axios.get.mockRejectedValueOnce(new Error('Network Error'));

    await expect(getSystemStats()).rejects.toThrow('Network Error');
  });
});
