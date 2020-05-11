import React from 'react';
import { Input } from '@ui-kitten/components';
import { useFormikContext } from 'formik';
import { AlertTriangleIcon } from '../../assets/icons';


export const FormInput = ({ id, ...inputProps }) => {

  const formContext = useFormikContext();

  // @ts-ignore
  const { [id]: error } = formContext.errors;

  const fieldProps = {
    status: error && 'danger',
    captionIcon: error && AlertTriangleIcon,
  };

  return (
    <Input
      {...inputProps}
      {...fieldProps}
      caption={error}
      onChangeText={formContext.handleChange(id)}
    />
  );
};

