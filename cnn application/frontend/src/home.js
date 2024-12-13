import React, { useState, useEffect } from "react";
import { makeStyles } from "@material-ui/core/styles";
import {
  AppBar,
  Toolbar,
  Typography,
  Container,
  Card,
  CardContent,
  Paper,
  CardActionArea,
  CardMedia,
  Grid,
  TableContainer,
  Table,
  TableBody, 
  TableHead,
  TableRow,
  TableCell,
  Button,
  CircularProgress
} from "@material-ui/core";

import { DropzoneArea } from 'material-ui-dropzone';
import { common } from '@material-ui/core/colors';
import Clear from '@material-ui/icons/Clear';
import axios from "axios";

// Background import
import image from "./bg.jpg";

const useStyles = makeStyles((theme) => ({
  root: {
    minHeight: '100vh',
    background: `linear-gradient(135deg, rgba(0,0,0,0.1), rgba(0,0,0,0.2)), url(${image})`,
    backgroundSize: 'cover',
    backgroundPosition: 'center',
    display: 'flex',
    flexDirection: 'column',
  },
  header: {
    background: 'rgba(255,255,255,0.1)', // Transparent header
    backdropFilter: 'blur(10px)', // Glassmorphism effect
    boxShadow: '0 2px 5px rgba(0,0,0,0.1)',
    padding: theme.spacing(1, 0),
  },
  headerTitle: {
    color: 'white',
    fontWeight: 600,
    textAlign: 'center',
    letterSpacing: '1px',
  },
  gridContainer: {
    flex: 1,
    display: 'flex',
    justifyContent: 'center',
    alignItems: 'center',
    padding: theme.spacing(4, 2),
  },
  imageCard: {
    maxWidth: 500,
    width: '100%', // Keep full width within the container
    margin: '0 auto', // Add this to center the card horizontally
    borderRadius: theme.spacing(3),
    backgroundColor: 'transparent',
    boxShadow: '0 10px 30px rgba(0,0,0,0.1)',
    transition: 'transform 0.3s ease',
    '&:hover': {
      transform: 'scale(1.02)',
    },
  },
  media: {
    height: 400,
    backgroundSize: 'cover',
  },
  clearButton: {
    marginTop: theme.spacing(2),
    background: 'linear-gradient(145deg, #f0f0f0, #e0e0e0)',
    color: '#333',
    fontWeight: 600,
    padding: theme.spacing(1.5, 3),
    borderRadius: theme.spacing(2),
    transition: 'transform 0.2s ease',
    '&:hover': {
      transform: 'scale(1.05)',
      background: 'linear-gradient(145deg, #e0e0e0, #f0f0f0)',
    },
  },
  tableContainer: {
    background: 'rgba(255,255,255,0.8)',
    borderRadius: theme.spacing(2),
    backdropFilter: 'blur(5px)',
    marginTop: theme.spacing(2),
  },
  loader: {
    color: theme.palette.primary.main,
    margin: theme.spacing(2),
  },
}));

export const ImageUpload = () => {
  const classes = useStyles();
  const [selectedFile, setSelectedFile] = useState();
  const [preview, setPreview] = useState();
  const [data, setData] = useState();
  const [image, setImage] = useState(false);
  const [isLoading, setIsloading] = useState(false);
  let confidence = 0;

  const sendFile = async () => {
    if (image) {
      setIsloading(true);
      let formData = new FormData();
      formData.append("file", selectedFile);

      try {
        let res = await axios({
          method: "post",
          url: process.env.REACT_APP_API_URL, 
          data: formData,
        });
        
        if (res.status === 200) {
          setData(res.data);
        }
      } catch (error) {
        console.error("File upload failed", error);
      } finally {
        setIsloading(false);
      }
    }
  };

  const clearData = () => {
    setData(null);
    setImage(false);
    setSelectedFile(null);
    setPreview(null);
  };

  useEffect(() => {
    if (!selectedFile) {
      setPreview(undefined);
      return;
    }
    const objectUrl = URL.createObjectURL(selectedFile);
    setPreview(objectUrl);

    return () => URL.revokeObjectURL(objectUrl);
  }, [selectedFile]);

  useEffect(() => {
    let isComponentMounted = true;

    if (preview && isComponentMounted) {
      sendFile();
    }

    return () => {
      isComponentMounted = false;
    };
  }, [preview]);

  const onSelectFile = (files) => {
    if (!files || files.length === 0) {
      setSelectedFile(undefined);
      setImage(false);
      setData(undefined);
      return;
    }
    setSelectedFile(files[0]);
    setData(undefined);
    setImage(true);
  };

  if (data) {
    confidence = (parseFloat(data.confidence) * 100).toFixed(2);
  }

  return (
    <div className={classes.root}>
      <AppBar position="static" className={classes.header} elevation={0}>
        <Toolbar>
          <Typography variant="h5" className={classes.headerTitle} fullWidth>
            Traffic Sign Detection 
          </Typography>
        </Toolbar>
      </AppBar>
      <Container maxWidth="md" className={classes.gridContainer}>
        <Grid container spacing={3} justifyContent="center">
          <Grid item xs={12}>
            <Card className={classes.imageCard}>
              {image && (
                <CardActionArea>
                  <CardMedia
                    className={classes.media}
                    image={preview}
                    title="Uploaded Image"
                  />
                </CardActionArea>
              )}
              {!image && (
                <CardContent>
                  <DropzoneArea
                    acceptedFiles={["image/*"]}
                    dropzoneText={
                      "Drag and drop an image of traffic to process"
                    }
                    onChange={onSelectFile}
                  />
                </CardContent>
              )}
              {data && (
                <CardContent>
                  <TableContainer component={Paper} className={classes.tableContainer}>
                    <Table>
                      <TableHead>
                        <TableRow>
                          <TableCell>Label:</TableCell>
                          <TableCell align="right">Confidence:</TableCell>
                        </TableRow>
                      </TableHead>
                      <TableBody>
                        <TableRow>
                          <TableCell>{data.class}</TableCell>
                          <TableCell align="right">{confidence}%</TableCell>
                        </TableRow>
                      </TableBody>
                    </Table>
                  </TableContainer>
                </CardContent>
              )}
              {isLoading && (
                <CardContent style={{ textAlign: 'center' }}>
                  <CircularProgress className={classes.loader} />
                  <Typography variant="h6">Processing</Typography>
                </CardContent>
              )}
            </Card>
          </Grid>
          {data && (
            <Grid item xs={12} style={{ textAlign: 'center' }}>
              <Button
                variant="contained"
                className={classes.clearButton}
                onClick={clearData}
                startIcon={<Clear />}
              >
                Clear
              </Button>
            </Grid>
          )}
        </Grid>
      </Container>
    </div>
  );
};