import * as Yup from 'yup';


export const ResetPasswordSchema = Yup.object().shape({
  email: Yup.string().email('Invalid email'),
});
