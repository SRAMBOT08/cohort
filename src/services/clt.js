import api from './api';

/**
 * CLT (Creative Learning Track) API Service
 * Handles all API calls for CLT submissions and file management
 */

const CLT_BASE = '/clt/submissions';

export const cltService = {
  /**
   * Get all submissions for the current user
   * @param {Object} params - Query parameters (page, page_size, etc.)
   * @returns {Promise} - Paginated list of submissions
   */
  getSubmissions: async (params = {}) => {
    const response = await api.get(CLT_BASE, { params });
    return response.data;
  },

  /**
   * Get a specific submission by ID
   * @param {number} id - Submission ID
   * @returns {Promise} - Submission details with files
   */
  getSubmission: async (id) => {
    const response = await api.get(`${CLT_BASE}/${id}/`);
    return response.data;
  },

  /**
   * Create a new CLT submission
   * @param {Object} data - Submission data
   * @param {string} data.title - Course title
   * @param {string} data.description - Course description
   * @param {string} data.platform - Learning platform
   * @param {string} data.completion_date - Completion date (YYYY-MM-DD)
   * @param {Array<File>} data.files - Optional files to upload
   * @returns {Promise} - Created submission
   */
  createSubmission: async (data) => {
    const formData = new FormData();
    formData.append('title', data.title);
    formData.append('description', data.description);
    formData.append('platform', data.platform);
    formData.append('completion_date', data.completion_date);

    // Add files if provided
    if (data.files && data.files.length > 0) {
      data.files.forEach((file) => {
        formData.append('files', file);
      });
    }

    const response = await api.post(CLT_BASE, formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
    });
    return response.data;
  },

  /**
   * Update an existing submission
   * @param {number} id - Submission ID
   * @param {Object} data - Fields to update
   * @returns {Promise} - Updated submission
   */
  updateSubmission: async (id, data) => {
    const response = await api.patch(`${CLT_BASE}/${id}/`, data);
    return response.data;
  },

  /**
   * Delete a submission (only draft or rejected)
   * @param {number} id - Submission ID
   * @returns {Promise}
   */
  deleteSubmission: async (id) => {
    const response = await api.delete(`${CLT_BASE}/${id}/`);
    return response.data;
  },

  /**
   * Upload additional files to an existing submission
   * @param {number} id - Submission ID
   * @param {Array<File>} files - Files to upload (max 10, 10MB each)
   * @returns {Promise} - Array of uploaded file objects
   */
  uploadFiles: async (id, files) => {
    const formData = new FormData();
    files.forEach((file) => {
      formData.append('files', file);
    });

    const response = await api.post(`${CLT_BASE}/${id}/upload_files/`, formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
    });
    return response.data;
  },

  /**
   * Submit a draft for review
   * @param {number} id - Submission ID
   * @returns {Promise} - Updated submission with status='submitted'
   */
  submitForReview: async (id) => {
    const response = await api.post(`${CLT_BASE}/${id}/submit/`);
    return response.data;
  },

  /**
   * Delete a specific file from a submission
   * @param {number} submissionId - Submission ID
   * @param {number} fileId - File ID to delete
   * @returns {Promise}
   */
  deleteFile: async (submissionId, fileId) => {
    const response = await api.delete(`${CLT_BASE}/${submissionId}/delete_file/`, {
      params: { file_id: fileId },
    });
    return response.data;
  },

  /**
   * Get submission statistics
   * @returns {Promise} - Stats object with counts by status
   */
  getStats: async () => {
    const response = await api.get(`${CLT_BASE}/stats/`);
    return response.data;
  },
};

export default cltService;
