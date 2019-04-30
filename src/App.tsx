import * as React from 'react';
import {useDropzone} from 'react-dropzone'
import * as superagent from "superagent";
import {FontAwesomeIcon} from '@fortawesome/react-fontawesome'
import {faFile, faFileAlt, faFileUpload} from '@fortawesome/free-solid-svg-icons'

export default class App extends React.Component<{}, {}> {
    render() {
        return <>
            {/*<DragList/>*/}
            <CapsuleForm/>
        </>;
    }
}

function CapsuleForm() {
    const [email1, setEmail1] = React.useState("");
    const [email2, setEmail2] = React.useState("");
    const [inviteRecipients, setInviteRecipients] = React.useState(false);
    const [policy, setPolicy] = React.useState(null);
    const [data, setData] = React.useState(null);

    const formSubmit = React.useCallback(() => {
        const req = superagent.post('http://127.0.0.1:5001/capsule')
            .field({email1})
            .field({email2})
            .field({inviteRecipients});

        if (policy !== null) {
            req.attach("policy", policy);
        }
        if (data !== null) {
            req.attach("data", data);
        }
        req.end();
    }, [email1, email2, inviteRecipients, policy, data]);

    const {getRootProps: getRootPropsPolicy, getInputProps: getInputPropsPolicy, isDragActive: isDragActivePolicy} = useDropzone({
        onDrop: React.useCallback((acceptedFiles: File[]) => setPolicy(acceptedFiles[0]), [policy])
    });

    const {getRootProps: getRootPropsData, getInputProps: getInputPropsData, isDragActive: isDragActiveData} = useDropzone({
        onDrop: React.useCallback((acceptedFiles: File[]) => setData(acceptedFiles[0]), [data])
    });

    return (
        <>
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
            <label> Invite Unregistered Recipients
                <input type="checkbox"
                       name="inviteRecipients"
                       onChange={e => setInviteRecipients(e.target.checked)}
                       checked={inviteRecipients}/>
            </label>
            <div {...getRootPropsPolicy()}>
                <label> Lua Policy
                    <input {...getInputPropsPolicy()} />
                    {
                        isDragActivePolicy ?
                            <>
                                <p>Release to upload your <strong>policy</strong> file</p>
                                <FontAwesomeIcon icon={faFileUpload} size="2x"/>
                            </> :
                            <>
                                <p>Drag & drop <strong>policy</strong> here, or click to select file</p>
                                <FontAwesomeIcon icon={faFileAlt} size="2x"/>
                            </>
                    }
                </label>
            </div>
            <div {...getRootPropsData()}>
                <label> Data
                    <input {...getInputPropsData()} />
                    {
                        isDragActiveData ?
                            <>
                                <p>Release to upload your <strong>attachment</strong></p>
                                <FontAwesomeIcon icon={faFileUpload} size="2x"/>
                            </> :
                            <>
                                <p>Drag & drop <strong>attachment</strong> here, or click to select file</p>
                                <FontAwesomeIcon icon={faFile} size="2x"/>
                            </>
                    }
                </label>
            </div>
            <button type="submit" onClick={formSubmit}>Submit</button>
        </>);
}
