import { useMemo } from "react";
import { useLocation } from "react-router-dom";

/**
 * The useQuery hook returns a memoized version of the query
 * parameters that changes based on which location is being
 * referenced.
 * 
 * The proper approach to use this hook is to declare as
 * follows:
 * 
 * let query = useQuery()
 * 
 * Usage:
 * 
 * query.get('department')
 */
const useQuery = () => {

    // Represents the current location.
    let params = useLocation();

    // Return the memoized set of key-value pairs as the
    // query search key as well as its value.
    return useMemo(() => {return new URLSearchParams(params)}, [params])

}

export default useQuery;