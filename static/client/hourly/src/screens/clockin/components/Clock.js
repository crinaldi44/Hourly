import React, {useEffect, useState} from "react";
import {CircularProgress} from "@mui/material";

/**
 * The Clock represents a live display of the current time.
 * @constructor
 */
const Clock = () => {

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
        let minutes = date.getMinutes().toLocaleString();
        let amPmString = 'AM'

        if (date.getHours() > 12) {
            hours = hours - 12
            amPmString = 'PM'
        }

        if (!loaded) setLoaded(true)

        return hours + ':' + minutes  + ' ' + amPmString
    }

    /**
     * Represents the current clock styling.
     * @type {{color: string, fontSize: string}}
     */
    const clockStyle = {
        color: 'var(--offwhite)',
        fontSize: '30px'
    }

    return(
        <div style={clockStyle}>
            {loaded ? currentTime : (<CircularProgress/>)}
        </div>
    );

}

export default Clock