import { useEffect, useState } from 'react';
import { getProfile } from '../api/profile';
import { getBusinessConfig } from '../config/businessConfigs';
import { BusinessContext } from './BusinessContextValue';

function readStorage(key, fallback = null) {
  try {
    return JSON.parse(localStorage.getItem(key) || JSON.stringify(fallback));
  } catch {
    localStorage.removeItem(key);
    return fallback;
  }
}

export function BusinessProvider({ children }) {
  const [profile, setProfile] = useState(() => readStorage('logimind-profile'));
  const [loading, setLoading] = useState(() => Boolean(readStorage('logimind-user')?.userId));

  useEffect(() => {
    const user = readStorage('logimind-user');
    if (!user?.userId) {
      return;
    }
    const localProfile = readStorage('logimind-profile');
    getProfile(user.userId).then((response) => setProfile(response.data)).catch(() => setProfile(localProfile)).finally(() => setLoading(false));
  }, []);

  return <BusinessContext.Provider value={{ profile, setProfile, loading, config: getBusinessConfig(profile?.businessType) }}>{children}</BusinessContext.Provider>;
}
