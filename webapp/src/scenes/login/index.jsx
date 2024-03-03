import { Box, Button, TextField } from "@mui/material";
import { Formik } from "formik";
import * as yup from "yup";
import useMediaQuery from "@mui/material/useMediaQuery";
import Header from "../../components/Header";

const Login = () => {
  const isNonMobile = useMediaQuery("(min-width:600px)");

  const handleFormSubmit = (values) => {
    // get environment variable from .env file
    const api_url = process.env.API_URL;

    const endpoint = `172.20.33.205/api/login`;

    let json = JSON.stringify(values);
    console.log('values', values);
    console.log('json', json);
    console.log('url', api_url);

    fetch(endpoint, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(values),
    })
    .then(response => {
      console.log('response', response);
      if (!response.ok) {
        throw new Error('Network response was not ok');
      }
      return response.json();
    })
    .then(data => {
      console.log(data);
      // Here you can handle the login success, e.g., redirecting the user or displaying a success message
    })
    .catch(error => {
      console.error('There was a problem with your fetch operation:', error);
      // Here you can handle errors, e.g., displaying an error message to the user
    });
  };

  return (
    <Box m="20px">
      <Header title="LOGIN" subtitle="Log into an existing account" />

      <Formik
        onSubmit={handleFormSubmit}
        initialValues={initialValues}
        validationSchema={checkoutSchema}
      >
        {({
          values,
          errors,
          touched,
          handleBlur,
          handleChange,
          handleSubmit,
        }) => (
          <form onSubmit={handleSubmit}>
            <Box
              display="grid"
              gap="30px"
              gridTemplateColumns="repeat(4, minmax(0, 1fr))"
              sx={{
                "& > div": { gridColumn: isNonMobile ? undefined : "span 4" },
              }}
            >
            <TextField
              fullWidth
              variant="filled"
              type="text"
              label="Email"
              onBlur={handleBlur}
              onChange={handleChange}
              value={values.email}
              name="email" // Make sure this matches the key in initialValues exactly
              error={!!touched.email && !!errors.email}
              helperText={touched.email && errors.email}
              sx={{ gridColumn: "span 2" }}
            />
            <TextField
              fullWidth
              variant="filled"
              type="text"
              label="Password"
              onBlur={handleBlur}
              onChange={handleChange}
              value={values.password}
              name="password" // Make sure this matches the key in initialValues exactly
              error={!!touched.password && !!errors.password} // Added error handling for the password field
              helperText={touched.password && errors.password} // Added helperText for the password field
              sx={{ gridColumn: "span 2" }}
            />

            </Box>
            <Box display="flex" justifyContent="end" mt="20px">
              <Button type="submit" color="secondary" variant="contained">
                Login
              </Button>
            </Box>
          </form>
        )}
      </Formik>
    </Box>
  );
};

const checkoutSchema = yup.object().shape({
  email: yup.string().email("invalid email").required("required"),
  password: yup.string().required("required"),
});

const initialValues = {
  email: "",
  password: "",
};

export default Login;