import * as Yup from 'yup';


export const SignUpSchema = Yup.object().shape({
  email: Yup.string().email('Invalid email'),
  password: Yup.string().min(8, 'Password must be at least 8 characters'),
  username: Yup.string().min(2, 'Username must be at least 2 characters'),
});

