import React, { useState } from 'react';
import './JobForm.css';

const JobForm = ({ onSubmit, loading, onReset }) => {
  const [formData, setFormData] = useState({
    title: '',
    company_profile: '',
    description: '',
    requirements: '',
    benefits: '',
    employment_type: '',
    required_experience: '',
    required_education: '',
    industry: '',
    function: '',
    location: '',
    telecommuting: 0,
    has_company_logo: 0,
    has_questions: 0,
  });

  const [showAdvanced, setShowAdvanced] = useState(false);

  const handleChange = (e) => {
    const { name, value, type, checked } = e.target;
    setFormData(prev => ({
      ...prev,
      [name]: type === 'checkbox' ? (checked ? 1 : 0) : value
    }));
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    onSubmit(formData);
  };

  const handleClear = () => {
    setFormData({
      title: '',
      company_profile: '',
      description: '',
      requirements: '',
      benefits: '',
      employment_type: '',
      required_experience: '',
      required_education: '',
      industry: '',
      function: '',
      location: '',
      telecommuting: 0,
      has_company_logo: 0,
      has_questions: 0,
    });
    onReset();
  };

  const loadExample = (type) => {
    if (type === 'real') {
      setFormData({
        title: 'Senior Software Engineer',
        company_profile: 'Google is a multinational technology company specializing in Internet-related services and products. We focus on innovation, user experience, and creating products that make a difference.',
        description: 'We are seeking a Senior Software Engineer to join our team working on large-scale distributed systems. You will design, develop, test, deploy, maintain, and improve software solutions. The ideal candidate has strong problem-solving skills and experience with modern technology stacks.',
        requirements: '- Bachelor\'s degree in Computer Science or equivalent practical experience\n- 5+ years of software development experience in Python, Java, or C++\n- Experience with distributed systems and cloud platforms (GCP, AWS)\n- Strong understanding of data structures and algorithms\n- Excellent communication and teamwork skills',
        benefits: 'Competitive salary, comprehensive health insurance, 401k matching, stock options, unlimited PTO, remote work flexibility, professional development budget, free meals and snacks',
        employment_type: 'Full-time',
        required_experience: 'Mid-Senior level',
        required_education: 'Bachelor\'s Degree',
        industry: 'Information Technology',
        function: 'Engineering',
        location: 'Mountain View, CA, US',
        telecommuting: 1,
        has_company_logo: 1,
        has_questions: 1,
      });
    } else {
      setFormData({
        title: 'WORK FROM HOME - EARN $5000/WEEK!!!',
        company_profile: '',
        description: 'AMAZING OPPORTUNITY!!! Make thousands of dollars per week from the comfort of your home! No experience needed! No interviews required! Just send us $99 for training materials and start earning TODAY!!! Limited spots available! ACT NOW!!! This is a legitimate business opportunity that will change your life!!!',
        requirements: 'Just need a computer and internet connection! Anyone can do this! No special skills required!',
        benefits: 'UNLIMITED INCOME POTENTIAL!!! Be your own boss! Work whenever you want! No supervision!',
        employment_type: 'Other',
        required_experience: 'Entry level',
        required_education: 'Unspecified',
        industry: 'Other',
        function: 'Other',
        location: '',
        telecommuting: 1,
        has_company_logo: 0,
        has_questions: 0,
      });
    }
  };

  return (
    <div className="job-form-container">
      <div className="form-header">
        <h2>📝 Job Posting Details</h2>
        <div className="example-buttons">
          <button type="button" onClick={() => loadExample('real')} className="btn-example real">
            Load Real Example
          </button>
          <button type="button" onClick={() => loadExample('fake')} className="btn-example fake">
            Load Fake Example
          </button>
        </div>
      </div>

      <form onSubmit={handleSubmit}>
        {/* Required Fields */}
        <div className="form-section">
          <h3>Required Information</h3>
          
          <div className="form-group">
            <label htmlFor="title">
              Job Title <span className="required">*</span>
            </label>
            <input
              type="text"
              id="title"
              name="title"
              value={formData.title}
              onChange={handleChange}
              placeholder="e.g. Senior Software Engineer"
              required
            />
          </div>

          <div className="form-group">
            <label htmlFor="description">
              Job Description <span className="required">*</span>
            </label>
            <textarea
              id="description"
              name="description"
              value={formData.description}
              onChange={handleChange}
              placeholder="Provide a detailed description of the job role, responsibilities, and what the candidate will be doing..."
              rows={6}
              required
            />
          </div>
        </div>

        {/* Optional Fields */}
        <div className="form-section">
          <h3>Additional Information (Optional but Recommended)</h3>
          
          <div className="form-row">
            <div className="form-group">
              <label htmlFor="company_profile">Company Profile</label>
              <textarea
                id="company_profile"
                name="company_profile"
                value={formData.company_profile}
                onChange={handleChange}
                placeholder="Brief description of the company..."
                rows={3}
              />
            </div>
          </div>

          <div className="form-row">
            <div className="form-group">
              <label htmlFor="requirements">Requirements</label>
              <textarea
                id="requirements"
                name="requirements"
                value={formData.requirements}
                onChange={handleChange}
                placeholder="Education, experience, skills required..."
                rows={4}
              />
            </div>

            <div className="form-group">
              <label htmlFor="benefits">Benefits</label>
              <textarea
                id="benefits"
                name="benefits"
                value={formData.benefits}
                onChange={handleChange}
                placeholder="Salary, insurance, perks offered..."
                rows={4}
              />
            </div>
          </div>

          <div className="form-row">
            <div className="form-group">
              <label htmlFor="location">Location</label>
              <input
                type="text"
                id="location"
                name="location"
                value={formData.location}
                onChange={handleChange}
                placeholder="e.g. New York, NY, US"
              />
            </div>

            <div className="form-group">
              <label htmlFor="employment_type">Employment Type</label>
              <select
                id="employment_type"
                name="employment_type"
                value={formData.employment_type}
                onChange={handleChange}
              >
                <option value="">Select...</option>
                <option value="Full-time">Full-time</option>
                <option value="Part-time">Part-time</option>
                <option value="Contract">Contract</option>
                <option value="Temporary">Temporary</option>
                <option value="Other">Other</option>
              </select>
            </div>
          </div>
        </div>

        {/* Advanced Fields */}
        <button
          type="button"
          className="toggle-advanced"
          onClick={() => setShowAdvanced(!showAdvanced)}
        >
          {showAdvanced ? '▼' : '▶'} Advanced Options
        </button>

        {showAdvanced && (
          <div className="form-section advanced">
            <div className="form-row">
              <div className="form-group">
                <label htmlFor="required_experience">Required Experience</label>
                <select
                  id="required_experience"
                  name="required_experience"
                  value={formData.required_experience}
                  onChange={handleChange}
                >
                  <option value="">Select...</option>
                  <option value="Internship">Internship</option>
                  <option value="Entry level">Entry Level</option>
                  <option value="Mid-Senior level">Mid-Senior Level</option>
                  <option value="Director">Director</option>
                  <option value="Executive">Executive</option>
                </select>
              </div>

              <div className="form-group">
                <label htmlFor="required_education">Required Education</label>
                <select
                  id="required_education"
                  name="required_education"
                  value={formData.required_education}
                  onChange={handleChange}
                >
                  <option value="">Select...</option>
                  <option value="High School or equivalent">High School</option>
                  <option value="Some College Coursework Completed">Some College</option>
                  <option value="Bachelor's Degree">Bachelor's Degree</option>
                  <option value="Master's Degree">Master's Degree</option>
                  <option value="Doctorate">Doctorate</option>
                  <option value="Unspecified">Unspecified</option>
                </select>
              </div>
            </div>

            <div className="form-row">
              <div className="form-group">
                <label htmlFor="industry">Industry</label>
                <input
                  type="text"
                  id="industry"
                  name="industry"
                  value={formData.industry}
                  onChange={handleChange}
                  placeholder="e.g. Information Technology"
                />
              </div>

              <div className="form-group">
                <label htmlFor="function">Function</label>
                <input
                  type="text"
                  id="function"
                  name="function"
                  value={formData.function}
                  onChange={handleChange}
                  placeholder="e.g. Engineering"
                />
              </div>
            </div>

            <div className="form-group checkboxes">
              <label className="checkbox-label">
                <input
                  type="checkbox"
                  name="telecommuting"
                  checked={formData.telecommuting === 1}
                  onChange={handleChange}
                />
                <span>Remote Work Available</span>
              </label>

              <label className="checkbox-label">
                <input
                  type="checkbox"
                  name="has_company_logo"
                  checked={formData.has_company_logo === 1}
                  onChange={handleChange}
                />
                <span>Has Company Logo</span>
              </label>

              <label className="checkbox-label">
                <input
                  type="checkbox"
                  name="has_questions"
                  checked={formData.has_questions === 1}
                  onChange={handleChange}
                />
                <span>Has Screening Questions</span>
              </label>
            </div>
          </div>
        )}

        {/* Action Buttons */}
        <div className="form-actions">
          <button type="submit" className="btn-submit" disabled={loading}>
            {loading ? 'Analyzing...' : '🔍 Analyze Job Posting'}
          </button>
          <button type="button" onClick={handleClear} className="btn-clear">
            Clear Form
          </button>
        </div>
      </form>
    </div>
  );
};

export default JobForm;
