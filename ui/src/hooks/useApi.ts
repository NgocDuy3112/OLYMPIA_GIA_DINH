/* eslint-disable @typescript-eslint/no-explicit-any */
import { useState, useCallback } from "react";

interface ApiOptions extends RequestInit {
    headers?: Record<string, string>;
}


interface ApiResult<T> {
    data: T | null;
    error: string | null;
    loading: boolean;
    refetch: () => Promise<void>;
}


export const useApi = <T = any>(url: string, options?: ApiOptions): ApiResult<T> => {
    const [data, setData] = useState<T | null>(null);
    const [error, setError] = useState<string | null>(null);
    const [loading, setLoading] = useState<boolean>(false);

    const fetchData = useCallback(async () => {
        setLoading(true);
        setError(null);
        try {
            const response = await fetch(url, options);
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            const result: T = await response.json();
            setData(result);
        } catch (err: any) {
            setError(err.message || "Unknown error");
        } finally {
            setLoading(false);
        }
    }, [url, options]);

    // Fetch once on hook mount
    // You can uncomment this if you want auto-fetch
    // useEffect(() => {
    //   fetchData();
    // }, [fetchData]);

    return { data, error, loading, refetch: fetchData };
};