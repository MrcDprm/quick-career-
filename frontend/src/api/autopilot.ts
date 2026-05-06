// AI Optimized by Skills Agent: Typed client for the final profile-to-LinkedIn-to-application workflow.
import { apiPost } from "./client";

export type CandidateProfilePayload = {
  personal: {
    full_name: string;
    email?: string;
    phone?: string;
    location?: string;
    links: string[];
  };
  summary: string;
  skills: string[];
  education: Array<{
    school: string;
    degree: string;
    field?: string;
    start_year?: number;
    end_year?: number;
  }>;
  certifications: Array<{
    name: string;
    issuer?: string;
    year?: number;
  }>;
  experiences: Array<{
    title: string;
    company: string;
    start_year?: number;
    end_year?: number;
    highlights: string[];
  }>;
  projects: Array<{
    name: string;
    description: string;
    technologies: string[];
  }>;
  languages: string[];
};

export type LinkedInJobFilters = {
  keywords: string[];
  location?: string;
  remote_only: boolean;
  experience_level?: string;
  limit: number;
  linkedin_search_url?: string;
  minimum_skill_matches: number;
};

export type AutopilotApplyRequest = {
  profile: CandidateProfilePayload;
  filters: LinkedInJobFilters;
  max_applications: number;
  submission_mode: "mock" | "email" | "platform";
};

export type AutopilotApplyResponse = {
  total_applications: number;
  summary: string;
  applications: Array<{
    job: {
      title: string;
      company: string;
      location: string;
      source_url: string;
      match_score: number;
      matched_skills: string[];
    };
    optimization: {
      match_score_before: number;
      match_score_after: number;
      highlighted_skills: string[];
      ats_resume_markdown: string;
      application_brief: string;
    };
    generated_resume: {
      file_name: string;
      content: string;
    };
    submission: {
      status: string;
      receipt?: string;
    };
  }>;
};

// AI Optimized by Skills Agent: Starts the complete autonomous application workflow.
export function runAutopilotApply(payload: AutopilotApplyRequest) {
  return apiPost<AutopilotApplyRequest, AutopilotApplyResponse>("/autopilot/apply", payload);
}
