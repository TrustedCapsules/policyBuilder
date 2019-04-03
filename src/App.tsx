import DragList from './DragList'
import * as React from "react";
import {useDropzone} from 'react-dropzone'
import * as superagent from "superagent";
import {FontAwesomeIcon} from '@fortawesome/react-fontawesome'
import {faFile, faDownload} from '@fortawesome/free-solid-svg-icons'

export default class App extends React.Component<{}, {}> {
    render() {
        return <>
            <DragList/>
            <MyDropzone/>
        </>;
    }
}

function MyDropzone() {
    const onDrop = React.useCallback((acceptedFiles: File[]) => {
        const req = superagent.post('http://127.0.0.1:5001/submit');
        acceptedFiles.forEach((file: File) => {
            console.log(file);
            req.attach(file.name, file);
        });
        req.end();
    }, []);
    const {getRootProps, getInputProps, isDragActive} = useDropzone({onDrop});

    return (
        <div {...getRootProps()}>
            <input {...getInputProps()} />
            {
                isDragActive ?
                    <>
                        <p>Drop the files here ...</p>
                        <FontAwesomeIcon icon={faFile} size="2x"/>
                    </> :
                    <>
                        <p>Drag 'n' drop some files here, or click to select files</p>
                        <FontAwesomeIcon icon={faDownload} size="2x"/>
                    </>
            }
        </div>
    )
}
