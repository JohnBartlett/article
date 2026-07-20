const BASE = 'https://api.cloudflare.com/client/v4';

function policyUrl({ accountId, appId, policyId }) {
  return `${BASE}/accounts/${accountId}/access/apps/${appId}/policies/${policyId}`;
}

async function callCf(url, opts, token, fetchFn) {
  const res = await fetchFn(url, {
    ...opts,
    headers: {
      Authorization: `Bearer ${token}`,
      'Content-Type': 'application/json',
      ...(opts.headers || {}),
    },
  });
  const data = await res.json();
  if (!res.ok || data.success === false) {
    const msg = data?.errors?.[0]?.message || `status ${res.status}`;
    throw new Error(`Cloudflare API error: ${msg}`);
  }
  return data.result;
}

async function getPolicy(config, fetchFn) {
  return callCf(policyUrl(config), { method: 'GET' }, config.token, fetchFn);
}

export async function getPolicyEmails(config, fetchFn = fetch) {
  const policy = await getPolicy(config, fetchFn);
  return (policy.include || [])
    .filter((r) => r.email && typeof r.email.email === 'string')
    .map((r) => r.email.email);
}

export async function setPolicyEmails(config, emails, fetchFn = fetch) {
  const policy = await getPolicy(config, fetchFn);
  const nonEmail = (policy.include || []).filter((r) => !r.email);
  const emailRules = emails.map((email) => ({ email: { email } }));
  const body = {
    ...policy,
    include: [...nonEmail, ...emailRules],
  };
  await callCf(policyUrl(config), { method: 'PUT', body: JSON.stringify(body) }, config.token, fetchFn);
}
