import { useEffect, useState } from 'react';
import { getProfile } from '../api/profile';
import { getBusinessConfig } from '../config/businessConfigs';
import { isBusinessType } from '../config/businessTypes';
import { BusinessContext } from './BusinessContextValue';

function readStorage(key, fallback = null) {
  try {
    return JSON.parse(localStorage.getItem(key) || JSON.stringify(fallback));
  } catch {
    localStorage.removeItem(key);
    return fallback;
  }
}

function normalizeProfile(profile) {
  if (!profile) return null;
  const businessType = isBusinessType(profile.businessType)
    ? profile.businessType
    : 'distributor';

  return { ...profile, businessType };
}

export function BusinessProvider({ children }) {
  const [profile, setProfile] = useState(() => normalizeProfile(readStorage('logimind-profile')));
  const [loading, setLoading] = useState(() => Boolean(readStorage('logimind-user')?.userId));

  useEffect(() => {
    const user = readStorage('logimind-user');
    if (!user?.userId) {
      return;
    }

    const localProfile = normalizeProfile(readStorage('logimind-profile'));
    getProfile(user.userId)
      .then((response) => setProfile(normalizeProfile(response.data)))
      .catch(() => setProfile(localProfile))
      .finally(() => setLoading(false));
  }, []);

  return <BusinessContext.Provider value={{ profile, setProfile: (nextProfile) => setProfile(normalizeProfile(nextProfile)), loading, config: getBusinessConfig(profile?.businessType) }}>{children}</BusinessContext.Provider>;
}
