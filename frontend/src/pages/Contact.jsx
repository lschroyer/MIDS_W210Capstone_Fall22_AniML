import React, { useState } from 'react'

const Contact = () => {
    const [name, setName] = useState('');
    const [email, setEmail] = useState('');
    const [message, setMessage] = useState('');
    const [emailSent, setEmailSent] = useState(false);

    const submit = () => {
        if (name && email && message) {
           // TODO - send mail
    
            setName('');
            setEmail('');
            setMessage('');
            setEmailSent(true);
        } else {
            alert('Please fill in all fields.');
        }
    }

    const isValidEmail = email => {
        const regex = /^(([^<>()\[\]\\.,;:\s@"]+(\.[^<>()\[\]\\.,;:\s@"]+)*)|(".+"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/;
        return regex.test(String(email).toLowerCase());
    };
    

    return (
        <>
            <br></br>
            <input type="text" placeholder="Your Name" value={name} onChange={e => setName(e.target.value)}/>
            <br></br>
            <input type="email" placeholder="Your email address" value={email} onChange={e => setEmail(e.target.value)} />
            <br></br>
            <textarea placeholder="Your message" value={message} onChange={e => setMessage(e.target.value)}></textarea>
            <button onClick={submit}>Send Message</button>
            <br></br>
            <span className={emailSent ? 'visible' : null}>Thank you for your message, we will be in touch in no time!</span>
        </>
    );
};

export default Contact;