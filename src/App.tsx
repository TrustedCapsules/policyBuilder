import DragList from './DragList'
import * as React from 'react';
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
    const [email1, setEmail1] = React.useState("");
    const [email2, setEmail2] = React.useState("");
    const [inviteRecipients, setInviteRecipients] = React.useState(false);
    const onDrop = React.useCallback((acceptedFiles: File[]) => {
        const req = superagent.post('http://127.0.0.1:5001/submit')
            .field({email1})
            .field({email2})
            .field({inviteRecipients});
        acceptedFiles.forEach((file: File) => req.attach(file.name, file));
        req.end();
    }, [email1, email2, inviteRecipients]);
    const {getRootProps, getInputProps, isDragActive} = useDropzone({onDrop});

    return (<>
        <label> Email 1
            <input type="email"
                   name="email1"
                   value={email1}
                   onChange={e => setEmail1(e.target.value)}
                   placeholder="Email 1"/>
        </label>
        <label> Email 2
            <input type="email"
                   name="email2"
                   value={email2}
                   onChange={e => setEmail2(e.target.value)}
                   placeholder="Email 2"/>
        </label>
        <input type="checkbox"
               name="inviteRecipients"
               onChange={e => setInviteRecipients(e.target.checked)}
               checked={inviteRecipients}/>
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
    </>);
}
