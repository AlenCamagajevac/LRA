import * as Yup from 'yup';

export class ResetPasswordData {

  constructor(email) { }

  static empty() {
    return new ResetPasswordData(
      '',
    );
  }
}


export const ResetPasswordSchema = Yup.object().shape({
  email: Yup.string().email('Invalid email'),
});
