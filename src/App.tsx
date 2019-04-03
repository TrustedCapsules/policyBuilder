import DragList from './DragList'
import * as React from "react";
import {useDropzone} from 'react-dropzone'
import * as superagent from "superagent";
import {library} from '@fortawesome/fontawesome-svg-core'
import {FontAwesomeIcon} from '@fortawesome/react-fontawesome'
import {faFile} from '@fortawesome/free-solid-svg-icons'


export default class App extends React.Component<{}, {}> {
    constructor(props: any) {
        super(props);
        library.add(faFile);
    }

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
                    <div>
                        <p>Drop the files here ...</p>
                        <FontAwesomeIcon icon="file"/>
                    </div> :
                    <p>Drag 'n' drop some files here, or click to select files</p>
            }
        </div>
    )
}
