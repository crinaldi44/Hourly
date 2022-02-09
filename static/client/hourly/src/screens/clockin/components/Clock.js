import React, {useEffect, useState} from "react";
import {CircularProgress} from "@mui/material";

/**
 * The Clock represents a live display of the current time.
 * @property style represents extra style elements to be passed
 */
const Clock = (props) => {

    // Represents the current time.
    const [currentTime, setCurrentTime] = useState('')

    // Represents whether the clock has been successfully loaded into memory.
    const [loaded, setLoaded] = useState(false)

    // On render, initiate a timed interval, fetch the new time every second.
    useEffect(() => {
        let clockInterval = setInterval(() => {

            setCurrentTime(getCurrentTime());

        }, 1000)

        return () => {
            clearInterval(clockInterval)
        }

    }, [])


    /**
     * Gets the current time.
     */
    const getCurrentTime = () => {

        // Fetch the current time in millis.
        let date = new Date();

        let hours = date.getHours();
        let minutes = date.getMinutes();
        let amPmString = 'AM'

        if (date.getHours() > 12) {
            hours = hours - 12
            amPmString = 'PM'
        }

        minutes = minutes < 10 ? (0 + minutes.toLocaleString()) : minutes.toLocaleString()

        if (!loaded) setLoaded(true)

        return hours + ':' + minutes  + ' ' + amPmString
    }

    /**
     * Represents the current clock styling.
     * @type {{color: string, fontSize: string}}
     */
    const clockStyle = {
        ...props.style,
        color: 'var(--offwhite)',
        fontSize: '40px',
        fontWeight: '700'
    }

    return(
        <div style={clockStyle}>
            {loaded ? currentTime : (<CircularProgress/>)}
        </div>
    );

}

export default Clock