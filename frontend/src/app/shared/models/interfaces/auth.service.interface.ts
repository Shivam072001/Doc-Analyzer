export interface User {
  username?: string;
  password?: string;
}

export interface AuthResponse {
  message: string;
  status: string;
  token?: string;
  username?: string;
}
