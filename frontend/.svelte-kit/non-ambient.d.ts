
// this file is generated — do not edit it


declare module "svelte/elements" {
	export interface HTMLAttributes<T> {
		'data-sveltekit-keepfocus'?: true | '' | 'off' | undefined | null;
		'data-sveltekit-noscroll'?: true | '' | 'off' | undefined | null;
		'data-sveltekit-preload-code'?:
			| true
			| ''
			| 'eager'
			| 'viewport'
			| 'hover'
			| 'tap'
			| 'off'
			| undefined
			| null;
		'data-sveltekit-preload-data'?: true | '' | 'hover' | 'tap' | 'off' | undefined | null;
		'data-sveltekit-reload'?: true | '' | 'off' | undefined | null;
		'data-sveltekit-replacestate'?: true | '' | 'off' | undefined | null;
	}
}

export {};


declare module "$app/types" {
	type MatcherParam<M> = M extends (param : string) => param is (infer U extends string) ? U : string;

	export interface AppTypes {
		RouteId(): "/" | "/bills" | "/contracts" | "/contracts/new" | "/contracts/[id]" | "/contracts/[id]/checkout" | "/contracts/[id]/renew" | "/properties" | "/properties/new" | "/properties/[id]" | "/properties/[id]/edit" | "/renewals" | "/repairs" | "/repairs/new" | "/tenants" | "/tenants/new" | "/tenants/[id]" | "/tenants/[id]/edit";
		RouteParams(): {
			"/contracts/[id]": { id: string };
			"/contracts/[id]/checkout": { id: string };
			"/contracts/[id]/renew": { id: string };
			"/properties/[id]": { id: string };
			"/properties/[id]/edit": { id: string };
			"/tenants/[id]": { id: string };
			"/tenants/[id]/edit": { id: string }
		};
		LayoutParams(): {
			"/": { id?: string | undefined };
			"/bills": Record<string, never>;
			"/contracts": { id?: string | undefined };
			"/contracts/new": Record<string, never>;
			"/contracts/[id]": { id: string };
			"/contracts/[id]/checkout": { id: string };
			"/contracts/[id]/renew": { id: string };
			"/properties": { id?: string | undefined };
			"/properties/new": Record<string, never>;
			"/properties/[id]": { id: string };
			"/properties/[id]/edit": { id: string };
			"/renewals": Record<string, never>;
			"/repairs": Record<string, never>;
			"/repairs/new": Record<string, never>;
			"/tenants": { id?: string | undefined };
			"/tenants/new": Record<string, never>;
			"/tenants/[id]": { id: string };
			"/tenants/[id]/edit": { id: string }
		};
		Pathname(): "/" | "/bills" | "/contracts" | "/contracts/new" | `/contracts/${string}/checkout` & {} | `/contracts/${string}/renew` & {} | "/properties" | "/properties/new" | `/properties/${string}/edit` & {} | "/renewals" | "/repairs" | "/repairs/new" | "/tenants" | "/tenants/new" | `/tenants/${string}/edit` & {};
		ResolvedPathname(): `${"" | `/${string}`}${ReturnType<AppTypes['Pathname']>}`;
		Asset(): string & {};
	}
}